# Deep Learning Feature Trees

This page outlines Backend Development Cost (BDC) analysis of Deep Learning accelerators. The Feature Tree Template (\<FT>) used for this analysis is available [below](#feature-tree-template). We used the provided \<FT> to model the following hardware:
* Unicore RISC-V CPU
* Intel Xeon CPU
* NVIDIA Fermi GPU
* NVIDIA Turing GPU
* Google TPU v1
* Versatile Tensor Accelerator (VTA)
* Intel Spring Hill
* NVIDIA Simba

## Feature Tree Template (\<FT>)



- **[System Root](#)** </br>  *combine =* SUM;  *weight =* 1 
  - **[Memory Hierarchy](#memory-hierarchy)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Implicit Data Movement](#memory-hierarchy--implicit-data-movement)**: No. of cache levels </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Explicit Data Movement](#memory-hierarchy--explicit-data-movement)**: No. of scratchpad levels </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Software Coherency](#memory-hierarchy--software-coherency)**: No. of software coherrent levels </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Data Access Granularity](#memory-hierarchy--data-access-granularity)**: No. of data access granularity levels </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Storage Properties](#memory-hierarchy--storage-properties)**: No. of storage properties [Activations, Weights, Output] </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
  - **[Node Types Set](#node-types-set)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Node](#node-types-set--node)** </br>  *combine =* SUM;  *weight =* 1 
      - **[Data Movement](#node-types-set--node--data-movement)** </br>  *combine =* SUM;  *weight =* 1 
        - **[DMA Engines](#node-types-set--node--data-movement--dma-engines)**: DMA engines present in node [y/n] </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Linear; *weight =* 1 
        - **[Stride](#node-types-set--node--data-movement--stride)**: No. of dimensions of hardware supported stride </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
        - **[Patterns](#node-types-set--node--data-movement--patterns)**: No. of movement patterns [Peer-to-Peer, Broadcast, Scatter] </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 
      - **[Control](#node-types-set--node--control)** </br>  *combine =* SUM;  *weight =* 1 
        - **[Indirect Addressing](#node-types-set--node--control--indirect-addressing)**: Node supports indirect addressing [y/n] </br> *stage_mask =* [0, 1, 0, 0];   *scale =* Linear; *weight =* 1 
        - **[Loop Levels](#node-types-set--node--control--loop-levels)**: No. of loop levels from full control flow </br> *stage_mask =* [0, 1, 0, 0];   *scale =* Linear; *weight =* 1 
        - **[Latency Hiding](#node-types-set--node--control--latency-hiding)**: No. of latency hiding widgets [Threads, Double Buffers] </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Exponential; *weight =* 1 
        - **[Data Dependency](#node-types-set--node--control--data-dependency)**: Sync. support between data producer and consumer </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
        - **[ISA Specialization](#node-types-set--node--control--isa-specialization)**: Avg no. of ISA commands per operator </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
      - **[Datapaths Set](#node-types-set--node--datapaths-set)** </br>  *combine =* SUM;  *weight =* 1 
        - **[DataPath](#node-types-set--node--datapaths-set--datapath)** </br>  *combine =* SUM;  *weight =* 1 
          - **[Operation Dimensions](#node-types-set--node--datapaths-set--datapath--operation-dimensions)**: No. of dimensions of data operations </br> *stage_mask =* [1, 0, 0, 0];   *scale =* Linear; *weight =* 1 
          - **[Unmaskable Dimensions](#node-types-set--node--datapaths-set--datapath--unmaskable-dimensions)**: No. of inner operation dimensions without masking support </br> *stage_mask =* [1, 0, 0, 0];   *scale =* Linear; *weight =* 1 
          - **[Memory Levels](#node-types-set--node--datapaths-set--datapath--memory-levels)**: No. of memory units in datapath [Input, Output, Internal] </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
          - **[Latency Hiding](#node-types-set--node--datapaths-set--datapath--latency-hiding)**: No. of latency hiding widgets [Threads, Double Buffers] </br> *stage_mask =* [0, 0, 1, 0];   *scale =* Linear; *weight =* 1 
  - **[Network and Synchronization](#network-and-synchronization)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Latency](#network-and-synchronization--latency)**: No. of latency domains visible to node </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Bandwidth](#network-and-synchronization--bandwidth)**: No. of bandwidth domains visible to node </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Topology Positions](#network-and-synchronization--topology-positions)**: No. of topology positions in node layout </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Sync Capability](#network-and-synchronization--sync-capability)**: No. of inter-node sync. capabilities [Atomics, Interrupt] </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 


## Backend Development Stages
TODO: Put diagram. discuss

## \<FT> Details
We now provide more details for the hardware features discussed in \<FT> above.

### Organization
The <FT> organizes Hardware Features Descriptors (HDFs) into following categories:
* Memory
* Node
    * Datapaths
    * Control
    * Data Movement
* Network and Synchronization

We differentiate between nodes and datapaths as follows. TODO: describe.

### Memory Hierarchy : Implicit Data Movement
This feature captures the number of cache levels in the memory hierarchy. Presence of cache is transparent to developers at functional stages. However, it is imperative for performance to employ loop tilling/blocking such that inner-most loop levels access data residing in closest cache levels.

### Memory Hierarchy : Explicit Data Movement
This feature captures the number of scratch levels in the memory hierarchy. Presence of scratchpads require developer attention even for the first functional version of backend. Hence, cache incurs BDC at all stages. 

### Memory Hierarchy : Software Coherency
Some levels of the memory hierarchy may delegate coherency management to the developer. The developer must ensure that multiple nodes accessing the same memory location can view the latest value. As cohrency is only relevant for multi-node scenarios, this feature incurs BDC at distributed backend development stages only.

### Memory Hierarchy : Data Access Granularity
Different memory levels may have different memory lines access granularity. While typically the memory line (or cache line) size is same throughout the memory hierarchy (order of bytes), modern high-capacity memories may present a bigger memory line size (order of few kilobytes). This mismatch may require additional considerations for optimization stages.

TODO: Explain diagram

### Memory Hierarchy : Storage Properties
Modern accelerators may specialize memory units to store only particular kinds of data. For example, Deep Learning accelerators dedicate some memory units to store activations while other memory units just to store weights. We use "Storage Properties" to refer to such memory specialization (which may extend beyond just weights or activations) as opposed to a homogenous memory unit. For the general case of operators which do not have a notion of weights and activations (such as concatanetaion), these storage properties require additional developer considerations during data placement and incur BDC at all stages of backend developement.

TODO: Explain diagram

### Node Types Set : Node : Data Movement : DMA Engines
Presence of DMA engines in a node opens up the possibility of an array of data movement scenarios concurrent with the node operation. Effectively using the DMAs requires additional developer considerations at optimization stages.

### Node Types Set : Node : Data Movement : Stride
Data movement problems can be formulated in different ways depending on the number of dimensions of stride supported by hardware. Higher number of stride dimensions increase the number of ways a data movement problem can be mapped to a data movement primitives. At the simplest extreme, no stride forces the developer to issue contiguous data movement commands. It is relevant to note that development for some operators working on high dimensional data may be eased by a higher stride dimension. Stride affects all single-node stages of backend development.

TODO: Explain diagram

### Node Types Set : Node : Data Movement : Patterns
Every multi-node system at least supports a peer-to-peer data movement primitive. More advanced patterns such as broadcast (multicast) or scatter/gather may also be supported by hardware. The number of possible formulations of a data movement problem can increase with the number of hardware supported data movement patterns. This feature is relevant in multi-node systems and impacts both distributed stages of backend development.

### Node Types Set : Node : Control : Indirect Addressing
If the nodes in a multi-node system support indirect addressing for memory access, the same instruction stream (indexed to appropriate data using node ID) can be executed at all the nodes involved. This can greatly simplify deployment of kernels across the distributed system of nodes. Indirect addressing also reduces the badnwidth requirements for instruction stream delivery to all nodes. This factor impacts the *func-dist* stage of backend development.

### Node Types Set : Node : Control : Loop Levels
Deep Learning accelerators may limit the control flow primitives supported at N inner-most loop levels for implementation simplicity and performance (reduced instruction stream bandwidth). This optimization requires the developer to formulate all instruction streams as at least N nested loops for best hardware utilization. This feature incurs BDC at *opt-single* stage.

### Node Types Set : Node : Control : Latency Hiding
Control at nodes may expose software managed latency hiding capabilities critical to ensure maximum hardware utilization. Some of the examples include hardware contexts for multithreading and software-managed double buffering. These latency hiding techniques are relevant at both optimization stages. 

Each of these latency hiding techniques interact with each other in complex ways which incurs a high BDC for full hardware utilizaiton. For example, implementing a multi-threaded implementation requires special developer effort; furthermore, properly managing double buffers in a multithreaded implementations is an even more daunting task. Hence, the BDC for this feature scales exponentially with *num_dims*.

### Node Types Set : Node : Control : Data Dependency


### Node Types Set : Node : Control : ISA Specialization


### Node Types Set : Node : Datapaths Set : Datapath : Operation Dimensions


### Node Types Set : Node : Datapaths Set : Datapath : Unmaskable Dimensions

### Node Types Set : Node : Datapaths Set : Datapath : Memory Levels


### Node Types Set : Node : Datapaths Set : Datapath : Latency Hiding

### Network and Synchronization : Latency
TODO: Per feature details here


### Network and Synchronization : Bandwidth


### Network and Synchronization : Topology Positions


### Network and Synchronization : Sync Capability


## References
TODO: Add
