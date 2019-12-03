from enum import Enum
import copy 
import sys, traceback
import logging
import statistics
import os, math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class Scale(Enum):
    LINEAR = 0
    EXP = 1
    LOG = 2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self is Scale.LINEAR:
            return "Linear"
        elif self is Scale.EXP:
            return "Exponential"
        else:
            return "Logarithmic"

    def scale_bdc(self, bdc):
        output = bdc

        # Linear is NOP here
        if self is Scale.EXP:
            output = 0 if bdc is 0 else math.exp(bdc)
        elif self is Scale.LOG:
            output = math.log(bdc)

        logging.debug("Scale={}, Input={}, Output={}".format(self.value, bdc, output))
        return output

# TODO: Consider if zeros should be included in average or not
class Combine(Enum):
    MEAN = 0
    MIN = 1
    MAX = 2
    SUM = 3

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def combine_bdc(self, lists):
        # lists is a list of bdc list
        num_lists = len(lists)
        if num_lists == 0:
            return None

        num_stages = len(lists[0])
        comb_list = [None] * num_stages

        if self is Combine.MEAN:
            # Temporarilty store sum here
            comb_list = copy.deepcopy(lists[0])
            for l in lists[1:]:
                # Accumulate values stage-wise
                for i in range(len(l)):
                    comb_list[i] += l[i]

            comb_list = [float(i) / num_lists for i in comb_list]

        if self is Combine.SUM:
            # Temporarilty store sum here
            comb_list = copy.deepcopy(lists[0])
            for l in lists[1:]:
                # Accumulate values stage-wise
                for i in range(len(l)):
                    comb_list[i] += l[i]

        elif self is Combine.MIN:
            # Store MIN so far
            comb_list = copy.deepcopy(lists[0])
            for l in lists[1:]:
                for i in range(len(l)):
                    comb_list[i] = comb_list[i] if comb_list[i] < l[i] else l[i]

        elif self is Combine.MAX:
            # Store MAX so far
            comb_list = copy.deepcopy(lists[0])
            for l in lists[1:]:
                for i in range(len(l)):
                    comb_list[i] = comb_list[i] if comb_list[i] > l[i] else l[i]

        logging.debug("Combine={}, Inputs={}, Output={}".format(self.value, lists, comb_list))
        return comb_list


# TODO: Add a tree validation check function
class Feature():

    def __init__(self,
                    name="default",
                    longname="Long Name",
                    description="The default feature description",
                    sub_features=[],
                    stage_mask=None,
                    weight=1,
                    scale=Scale.LINEAR,
                    combine=None):

        # Feature properties
        self.name = name
        self.longname = longname
        self.description = description

        self.stage_mask = stage_mask
        self.weight = weight
        self.scale = scale

        self.combine = combine
        self.sub_features = sub_features
    
        # The actual values of this Feature
        self.num_dims = None
        self.bdc = None


    def is_leaf_node(self):
        return len(self.sub_features) == 0


    # TODO: check conditions of leaf/middle when setting values
    def init(self, **kwargs):
        for key, value in kwargs.items():
            logging.debug("Setting {}={} for {}".format(key, value, self.name))
            if key is "stage_mask":
                self.stage_mask = value
            elif key is "combine":
                self.combine = value
            elif key is "num_dims":
                self.num_dims = value
            elif key is "scale":
                self.scale = value
            elif key is "weight":
                self.weight = value
            elif key is "name":
                self.name = value
            elif key is "description":
                self.description = value
            else:
                logging.error("Invalid key provided to Feature.init()")


    # Combine all values to come up with BDC numbers
    def eval_bdc(self, stage_filter):

        # This flag is for debugging only.
        # Set this to 5 for proper BDC calculuation
        subj_level = 5

        # Ignore all multi related fields if this is single PE design

        pre_weight_bdc = None

        if self.is_leaf_node():

            # Level 1: Direction
            bdc_masked = [i * self.num_dims for i in self.stage_mask]

            # Apply any initialization specific stage filters
            bdc_masked = stage_filter(bdc_masked)
            
            # Level 5: Scaling
            if subj_level >= 5:
                bdc_scaled = [self.scale.scale_bdc(i) for i in bdc_masked]
            else:
                bdc_scaled = bdc_masked

            pre_weight_bdc = bdc_scaled
        else:

            # Level 3: Combine BDCs from sub-features
            sub_bdc = []
            # First evaluate and fetch bdc values from all children
            for f in self.sub_features:
                sub_bdc.append(f.eval_bdc(stage_filter))
            # Apply combination method
            bdc_combined = self.combine.combine_bdc(sub_bdc)

            pre_weight_bdc = bdc_combined

        # Level 4: Assign weights to BDCs before returning them
        if subj_level >= 4:
            bdc_final = [i * self.weight for i in pre_weight_bdc]
        else:
            bdc_final = pre_weight_bdc

        self.bdc = bdc_final

        # Round everything 1 decimal point.
        self.bdc = [ (round(elem, 1) if (elem is not None) else None) for elem in self.bdc]

        return self.bdc


    def to_stdout(self, tree_level=0):
        # This flag is for debugging only.
        # Set this to 5 for proper BDC calculuation
        subj_level = 5

        out = "{}{} - {} - {}".format("    "*tree_level, self.name, self.longname, self.description)
        
        # Only applicable for leaf nodes
        if subj_level >= 2 and self.is_leaf_node():
            out += ", stage_mask={}".format(self.stage_mask)

        # Not applicable for leaf nodes
        if subj_level >= 3 and not self.is_leaf_node():
            out += ", combine={}".format(self.combine)

        if subj_level >= 4:
            out += ", weight={}".format(self.weight)

        # Only applied to value leaf nodes
        if subj_level >= 5 and self.is_leaf_node():
            out += ", scale={}".format(self.scale)

        # Print BDC values per stage
        out += ", bdc={}".format(self.bdc)

        # Print num_dims
        if self.is_leaf_node():
            out += ", num_dims={}".format(self.num_dims)

        for f in self.sub_features:
            out += "\n{}".format(f.to_stdout(tree_level+1))

        return out

    def lookup_subfeature(self, sub_find):
        for f in self.sub_features:
            if f.name == sub_find:
                return f

        raise KeyError(sub_find)

    def to_stdout_leaf_nodes(self, breadcrumb):
        out = ""
        if self.is_leaf_node():
            out = "{}.{}\n".format(breadcrumb, self.name)
        else:
            for f in self.sub_features:
                out += f.to_stdout_leaf_nodes("{}.{}".format(breadcrumb, self.name))

        return out

    # Lookup a feature in sub-tree from its path string
    def find_sub_f(self, feature_path):
        logging.debug("Accessing feature list: {}".format(feature_path))
        path = feature_path.split(".")

        # Make sure split was reasonable
        if len(path) == 1:
            if (self.name == feature_path):
                return [self]
            else:
                raise(KeyError())

        # Find the right child
        cur_list = [self]
        for f in path[1:]:
            if f == "*":
                # We should only get 1 * wildcard character
                cur_list = cur_list[0].sub_features
            else:
                new_list = []
                for n in cur_list:
                    for subs in n.sub_features:
                        if subs.name == f:
                            new_list.append(subs)
                cur_list = new_list
        
        return cur_list

    def get_sub_f_bdc(self):
        # Collect all children BDCs
        out = []
        for f in self.sub_features:
            out.append(f.bdc)

        return out

    def get_sub_f_desc(self):
        # Collect all children names
        desc = []
        for f in self.sub_features:
            desc.append(f.description)

        return desc


class FeatureTree():

    def __init__(self):
        self.name = "Default HW Name"

        self.root = None
        self.stages = None


    def find_sub_f(self, feature_path):
        logging.debug("Feature Tree = {}: ".format(self.name))
            
        return self.root.find_sub_f(feature_path)


    def access_conditions(self):
        if self.root is None:
            logging.error("Error: Cannot access Feature Tree!")
            return "Error"


    def eval(self):
        self.access_conditions()
        self.root.eval_bdc(self.stage_filter)
        return self.root.bdc


    def get_bdc(self):
        return self.root.bdc


    def stage_filter(self, bdc):
        # No default stage filter
        return bdc


    def get_categories(self):
        # Sub features of root are categories
        return self.root.get_sub_f_desc()


    def get_category_bdc(self):
        # Return BDCs from sub-childreen of root
        return copy.deepcopy(self.root.get_sub_f_bdc())


    def to_stdout(self):
        self.access_conditions()

        return ("Feature Tree: Name = {}\n"
                "BDC = {}\n\n{}\n").format( self.name,
                    self.root.bdc,
                    self.root.to_stdout())
