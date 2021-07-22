module example_mod(
    input ref_clk
   ,input sys_rstn
   ,input global_cg_enable
   ,output  [7:0] dbg_bus
   ,output        error_fiq
   ,input          cpucore_mst_ACLK
   ,input          cpucore_mst_ARESETn
   ,output [31:0]  cpucore_mst_AWADDR
   ,output [7:0]   cpucore_mst_AWID
   ,output         cpucore_mst_AWVALID
   ,input          cpucore_mst_AWREADY
   ,output [3:0]   cpucore_mst_AWSIZE
   ,output [3:0]   cpucore_mst_AWLEN
   ,output [31:0]  cpucore_mst_ARADDR
   ,output [7:0]   cpucore_mst_ARID
   ,output         cpucore_mst_ARVALID
   ,input          cpucore_mst_ARREADY
   ,output [3:0]   cpucore_mst_ARSIZE
   ,output [3:0]   cpucore_mst_ARLEN
   ,output [127:0] cpucore_mst_WDATA
   ,output [15:0]  cpucore_mst_WSTRB
   ,output         cpucore_mst_WLAST
   ,output         cpucore_mst_WVALID
   ,input          cpucore_mst_WREADY
   ,input  [7:0]   cpucore_mst_BID
   ,input  [1:0]   cpucore_mst_BRESP
   ,input          cpucore_mst_BVALID
   ,output         cpucore_mst_BREADY
   ,input  [7:0]   cpucore_mst_RID
   ,input  [127:0] cpucore_mst_RDATA
   ,input  [1:0]   cpucore_mst_RRESP
   ,input          cpucore_mst_RLAST
   ,input          cpucore_mst_RVALID
   ,output         cpucore_mst_RREADY
   ,input          syscsr_slv_ACLK
   ,input          syscsr_slv_ARESETn
   ,input  [31:0]  syscsr_slv_AWADDR
   ,input  [7:0]   syscsr_slv_AWID
   ,input          syscsr_slv_AWVALID
   ,output         syscsr_slv_AWREADY
   ,input  [3:0]   syscsr_slv_AWSIZE
   ,input  [3:0]   syscsr_slv_AWLEN
   ,input  [31:0]  syscsr_slv_ARADDR
   ,input  [7:0]   syscsr_slv_ARID
   ,input          syscsr_slv_ARVALID
   ,output         syscsr_slv_ARREADY
   ,input  [3:0]   syscsr_slv_ARSIZE
   ,input  [3:0]   syscsr_slv_ARLEN
   ,input  [127:0] syscsr_slv_WDATA
   ,input  [15:0]  syscsr_slv_WSTRB
   ,input          syscsr_slv_WLAST
   ,input          syscsr_slv_WVALID
   ,output         syscsr_slv_WREADY
   ,output [7:0]   syscsr_slv_BID
   ,output [1:0]   syscsr_slv_BRESP
   ,output         syscsr_slv_BVALID
   ,input          syscsr_slv_BREADY
   ,output [7:0]   syscsr_slv_RID
   ,output [127:0] syscsr_slv_RDATA
   ,output [1:0]   syscsr_slv_RRESP
   ,output         syscsr_slv_RLAST
   ,output         syscsr_slv_RVALID
   ,input          syscsr_slv_RREADY

);


endmodule
