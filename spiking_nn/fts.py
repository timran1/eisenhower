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
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_access_gran")] # Cache block size, reg size
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
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("avx.latency_hide")]    # threading contexts, sw managed double buffering

        return vector_datapath

####
class NVIDIA_Fermi_GPU(CPU):

    def __init__(self):
        super().__init__()
        self.name = "NVIDIA Fermi"

        try:

            # Extend utilizability to include any special HW features
            # Add vector datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(datapath_template)
            datapaths_set.sub_features.append(NVIDIA_Fermi_GPU.get_cuda_datapath(datapath_template))

            # Memory
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]  # L2 / global
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")]   # Reg file, L1 (cache/scratc)
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_props")]  # Cache vs scratch

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")]   # Thread
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")] # SW based

            # Network: L1 is local to each SM. Making a NUMA-like situation
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_latency")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_bandwidth")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_cuda_datapath(template):

        vector_datapath = copy.deepcopy(template)
        vector_datapath.init(name="cuda", description="CUDA Datapath")

        [f.init(num_dims=2) for f in vector_datapath.find_sub_f("cuda.num_dims_operation")]
        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("cuda.num_dims_mask")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("cuda.num_mem_levels")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("cuda.latency_hide")]

        return vector_datapath


class Loihi(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Intel Loihi"

        try:

            # Extend utilizability to include any special HW features
            # Add ALU and GEMM datapaths
            # Remove Scalar datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            # datapaths_set.sub_features.remove(scalar_datapath)
            # datapaths_set.sub_features.append(Simba.get_simba_pe_datapath(scalar_datapath))
            # datapaths_set.sub_features.append(Simba.get_global_pe_scalar_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")] # L1: Input, weight, output, L2 = Global PE
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]

            # Node - Global PE
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA exists
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]    # 2D stride (assumed)
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_pattern")] # Unicast, Multicast
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # Can work on global PE directly
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.indirect_addr")]  # Yes 
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # ?
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # SW only

            # Network
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_latency")]  # package level
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_bandwidth")]  # package level
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_topology")]  # 3 possible positions
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]   # Atomic access

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    # @staticmethod
    # def get_simba_pe_datapath(template):

    #     datapath = copy.deepcopy(template)
    #     datapath.init(name="simba_pe", description="Simba PE Datapath")

    #     [f.init(num_dims=3) for f in datapath.find_sub_f("simba_pe.num_dims_operation")]
    #     [f.init(num_dims=2) for f in datapath.find_sub_f("simba_pe.num_dims_mask")]
    #     [f.init(num_dims=1) for f in datapath.find_sub_f("simba_pe.num_mem_levels")]
    #     [f.init(num_dims=0) for f in datapath.find_sub_f("simba_pe.latency_hide")]

    #     return datapath

    # @staticmethod
    # def get_global_pe_scalar_datapath(template):

    #     datapath = copy.deepcopy(template)
    #     datapath.init(name="global_pe_scalar", description="Global PE Scalar Datapath")

    #     [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.num_dims_operation")]
    #     [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.num_dims_mask")]
    #     [f.init(num_dims=1) for f in datapath.find_sub_f("global_pe_scalar.num_mem_levels")]
    #     [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.latency_hide")]

    #    return datapath

