from feature_tree import *


class DeepLearning_FT_Template(FeatureTree):

    def __init__(self):
        super().__init__()

        # Hardware Feature Descriptors

        # name
        ##########################
        self.root = Feature(
            "system", "System Root", "", [
            
                Feature("memory", "Memory Hierarchy", "", [
                    Feature("num_cache",        "Implicit Data Movement",   "No. of cache levels"),
                    Feature("num_scratch",      "Explicit Data Movement",   "No. of scratchpad levels"),
                    Feature("num_sw_coherent",  "Software Coherency",       "No. of software coherrent levels"),
                    Feature("num_access_gran",  "Data Access Granularity",  "No. of data access granularity levels"),
                    Feature("num_props",        "Storage Properties",       "No. of storage properties [Activations, Weights, Output]"),
                ]),
                
                Feature("nodetypes_set", "Node Types Set", "", [
                    Feature("node", "Node", "", [
                        Feature("data_mov", "Data Movement", "", [
                            Feature("local_dma",   "DMA Engines",   "DMA engines present in node [y/n] "),
                            Feature("num_stride",  "Stride",        "No. of dimensions of hardware supported stride"),
                            Feature("num_pattern", "Patterns",      "No. of movement patterns [Peer-to-Peer, Broadcast, Scatter]"),
                        ]),
                        Feature("control", "Control", "", [
                            Feature("indirect_addr", "Indirect Addressing",     "Node supports indirect addressing [y/n]"),
                            Feature("loop_levels",   "Loop Levels ",            "No. of loop levels from full control flow"),
                            Feature("latency_hide",  "Latency Hiding",          "No. of latency hiding widgets [Threads, Double Buffers]"),
                            Feature("data_dep",      "Data Dependency",         "Sync. support between data producer and consumer"),
                            Feature("isa_decomp",    "ISA Specialization",      "Avg no. of ISA commands per operator"),
                        ]),
                        Feature("datapaths_set", "Datapaths Set", "", [
                            Feature("datapath", "DataPath", "", [
                                Feature("num_dims_operation", "Operation Dimensions",   "No. of dimensions of data operations"),
                                Feature("num_dims_mask",      "Unmaskable Dimensions",  "No. of inner operation dimensions without masking support"),
                                Feature("num_mem_levels",     "Memory Levels",          "No. of memory units in datapath [Input, Output, Internal]"),
                                Feature("latency_hide",       "Latency Hiding",         "No. of latency hiding widgets [Threads, Double Buffers]"),
                            ]),
                        ]),
                    ]),
                ]),

                Feature("network", "Network and Synchronization", "", [
                    Feature("num_latency",        "Latency",            "No. of latency domains visible to node"),
                    Feature("num_bandwidth",      "Bandwidth",          "No. of bandwidth domains visible to node"),
                    Feature("num_topology",       "Topology Positions", "No. of topology positions in node layout"),
                    Feature("num_sync_capability","Sync Capability",    "No. of inter-node sync. capabilities [Atomics, Interrupt]"),
                ]),

            ])
        

        try:
            
            # stage_mask
            # combine
            ##########################
            self.stages =              ["func-single", "func-dist", "opt-single",  "opt-dist"]
            # Some helper variables for commonly seen impact stage_masktions
            self.MASK_ALL_SET =        [1, 1, 1, 1]
            self.MASK_FUNC_ONLY_SET  = [1, 1, 0, 0]
            self.MASK_OPT_ONLY_SET   = [0, 0, 1, 1]
            self.MASK_MULTI_ONLY_SET = [0, 1, 0, 1]
            self.MASK_SINGL_ONLY_SET = [1, 0, 1, 0]

            # Set everything stage_mask=[1,1,1,1] and combine=MEAN
            [f.init(combine=Combine.SUM) for f in self.find_sub_f("system")]
            [f.init(combine=Combine.SUM) for f in self.find_sub_f("system.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.memory.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.node.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.node.control.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath.*")]
            [f.init(stage_mask=self.MASK_ALL_SET, combine=Combine.SUM) for f in self.find_sub_f("system.network.*")]

            # Set memory features
            memory = self.find_sub_f("system.memory")[0]
            memory.find_sub_f("memory.num_cache")[0].init(      stage_mask=self.MASK_OPT_ONLY_SET)
            memory.find_sub_f("memory.num_scratch")[0].init(    stage_mask=self.MASK_ALL_SET)
            memory.find_sub_f("memory.num_sw_coherent")[0].init(stage_mask=self.MASK_MULTI_ONLY_SET)
            memory.find_sub_f("memory.num_props")[0].init(      stage_mask=self.MASK_SINGL_ONLY_SET)
            memory.find_sub_f("memory.num_access_gran")[0].init(stage_mask=self.MASK_ALL_SET)

            # Set node template
            node = self.find_sub_f("system.nodetypes_set.node")[0]
            node.find_sub_f("node.data_mov.local_dma")[0].init(     stage_mask=self.MASK_OPT_ONLY_SET)
            node.find_sub_f("node.data_mov.num_stride")[0].init(    stage_mask=self.MASK_SINGL_ONLY_SET)
            node.find_sub_f("node.data_mov.num_pattern")[0].init(   stage_mask=self.MASK_MULTI_ONLY_SET)
            node.find_sub_f("node.control.loop_levels")[0].init(    stage_mask=[0, 1, 0, 0])
            node.find_sub_f("node.control.indirect_addr")[0].init(  stage_mask=[0, 1, 0, 0])
            node.find_sub_f("node.control.latency_hide")[0].init(   stage_mask=self.MASK_OPT_ONLY_SET)
            node.find_sub_f("node.control.data_dep")[0].init(       stage_mask=self.MASK_SINGL_ONLY_SET)
            node.find_sub_f("node.control.isa_decomp")[0].init(     stage_mask=self.MASK_ALL_SET)

            # Set datapath template
            datapath = node.find_sub_f("node.datapaths_set.datapath")[0]
            datapath.find_sub_f("datapath.num_dims_operation")[0].init( stage_mask=[1, 0, 0, 0])
            datapath.find_sub_f("datapath.num_dims_mask")[0].init(      stage_mask=[1, 0, 0, 0])
            datapath.find_sub_f("datapath.num_mem_levels")[0].init(     stage_mask=[1, 0, 1, 0])
            datapath.find_sub_f("datapath.latency_hide")[0].init(       stage_mask=[0, 0, 1, 0])

            # Network features
            network = self.find_sub_f("system.network")[0]
            network.find_sub_f("network.num_latency")[0].init(          stage_mask=[0, 0, 0, 1])
            network.find_sub_f("network.num_bandwidth")[0].init(        stage_mask=[0, 0, 0, 1])
            network.find_sub_f("network.num_topology")[0].init(         stage_mask=[0, 0, 0, 1])
            network.find_sub_f("network.num_sync_capability")[0].init(  stage_mask=self.MASK_MULTI_ONLY_SET)


            # weight
            # scale
            ##########################
            node = self.find_sub_f("system.nodetypes_set.node")[0]
            node.find_sub_f("node.control.latency_hide")[0].init(scale=Scale.EXP)



            # num_dims
            ##########################
            # Assign everything to 0

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_scratch")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_sw_coherent")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_access_gran")]

            # Node
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_pattern")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.indirect_addr")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.isa_decomp")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath.num_dims_operation")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath.num_dims_mask")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath.num_mem_levels")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath.latency_hide")]

            # Network and Synchronization
            [f.init(num_dims=0) for f in self.find_sub_f("system.network.num_latency")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.network.num_bandwidth")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.network.num_topology")]
            [f.init(num_dims=0) for f in self.find_sub_f("system.network.num_sync_capability")]

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    # Filter out impact of particular stages based on values of some features
    # This function is automatically called when doing bdc eval
    def stage_filter(self, bdc):

        # If latency is zero, it is a single PE design
        if self.find_sub_f("system.network.num_latency")[0].num_dims == 0:
            bdc[1] = 0
            bdc[3] = 0

        return bdc

    # What are the define "Categories"
    def get_categories(self):
        # Sub features of root are categories
        cats = [
            "Memory",
            "Network",
            "Control",
            "Datapaths",
            "Data Mov."
        ]
        return cats

    # Method to extract BDCs for each defined "Categories".
    def get_category_bdc(self):
        # Return BDCs from sub-childreen of root
        cats = []
        cats.append(self.find_sub_f("system.memory")[0].bdc)
        cats.append(self.find_sub_f("system.network")[0].bdc)

        # Collect 3 aspects of node: control, movement, datapath
        cats.append([0] * len(cats[0]))
        cats.append([0] * len(cats[0]))
        cats.append([0] * len(cats[0]))

        node_set = self.find_sub_f("system.nodetypes_set")[0]
        for node in node_set.find_sub_f("nodetypes_set.*"):
            node_name = node.name
            control = node.find_sub_f(node_name + ".control")[0].bdc
            datapaths = node.find_sub_f(node_name + ".datapaths_set")[0].bdc
            move = node.find_sub_f(node_name + ".data_mov")[0].bdc

            for i in range (len(control)):
                cats[2][i] += control[i]
                cats[3][i] += datapaths[i]
                cats[4][i] += move[i]

        return copy.deepcopy(cats)

