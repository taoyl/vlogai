// AXI4 Slave interface
interface axi4mst(
    input          ACLK
   ,input          ARESETn
   ,output [31:0]  AWADDR
   ,output [7:0]   AWID
   ,output         AWVALID
   ,input          AWREADY
   ,output [3:0]   AWSIZE
   ,output [3:0]   AWLEN
   ,output [31:0]  ARADDR
   ,output [7:0]   ARID
   ,output         ARVALID
   ,input          ARREADY
   ,output [3:0]   ARSIZE
   ,output [3:0]   ARLEN
   ,output [127:0] WDATA
   ,output [15:0]  WSTRB
   ,output         WLAST
   ,output         WVALID
   ,input          WREADY
   ,input  [7:0]   BID
   ,input  [1:0]   BRESP
   ,input          BVALID
   ,output         BREADY
   ,input  [7:0]   RID
   ,input  [127:0] RDATA
   ,input  [1:0]   RRESP
   ,input          RLAST
   ,input          RVALID
   ,output         RREADY
);
endinterface
