from ft_template import *


####
class CPU(SpikingNN_FT_Template):

    def __init__(self):
        super().__init__()
        self.name = "Unicore RISCV"

        try:

            # Extend utilizability to include any special HW features
            # CPU has multiple types of datapaths
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath")[0]
            datapaths_set.sub_features.remove(datapath_template)
            datapaths_set.sub_features.append(CPU.get_scalar_datapath(datapath_template))

            # Assign values to remaining features
            ##

            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")] # SW based

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_scalar_datapath(template):

        scalar_datapath = copy.deepcopy(template)
        scalar_datapath.init(name="scalar", description="Scalar Datapath")

        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_operation")]
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_mask")]
        [f.init(num_dims=1) for f in scalar_datapath.find_sub_f("scalar.num_mem_levels")]   # Normal registers
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.latency_hide")]

        return scalar_datapath

####
class Intel_Xeon_Skylake_CPU(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Xeon Skylake"

        try:

            # Add vector datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.scalar")[0]
            datapaths_set.sub_features.append(Intel_Xeon_Skylake_CPU.get_avx_datapath(datapath_template))

            # Assign values to remaining features
            ##
            [f.init(num_dims=3) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_gran")] # minimum byte/work level ops
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # thread

            # Network: NUMA nodes in single socket
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_latency")]   # SNC, NUMA
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_bandwidth")]   # SNC, NUMA
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_topology")]  # Linear layout
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_sync_capability")]   # atomic, interrupt

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    @staticmethod
    def get_avx_datapath(template):

        vector_datapath = copy.deepcopy(template)
        vector_datapath.init(name="avx", description="AVX Datapath")

        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("avx.num_dims_operation")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("avx.num_dims_mask")]
        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("avx.num_mem_levels")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("avx.latency_hide")]

        return vector_datapath

class Loihi(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Intel Loihi"

        try:

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]

            # Node
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_grans")]  # bit level msging as well
            [f.init(num_dims=3) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_pattern")] # Unicast, Multicast, Scatter
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # Can work on global PE directly
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # Fan-in / Fan-out

            # Network
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_latency")]  # 2 networks on chip, intra-neuromorphic core
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_bandwidth")]  # same as above
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_topology")]  # 3 possible positions in 2d grid
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]   # Only async access

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    @staticmethod
    def get_scalar_datapath(template):

        scalar_datapath = copy.deepcopy(template)
        scalar_datapath.init(name="scalar", description="Scalar Datapath")

        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_operation")]
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_mask")]
        [f.init(num_dims=1) for f in scalar_datapath.find_sub_f("scalar.num_mem_levels")]   # Normal registers
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.latency_hide")]

        return scalar_datapath

