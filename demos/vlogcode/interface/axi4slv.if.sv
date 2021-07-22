// AXI4 Slave interface
interface axi4slv(
    input          ACLK
   ,input          ARESETn
   ,input  [31:0]  AWADDR
   ,input  [7:0]   AWID
   ,input          AWVALID
   ,output         AWREADY
   ,input  [3:0]   AWSIZE
   ,input  [3:0]   AWLEN
   ,input  [31:0]  ARADDR
   ,input  [7:0]   ARID
   ,input          ARVALID
   ,output         ARREADY
   ,input  [3:0]   ARSIZE
   ,input  [3:0]   ARLEN
   ,input  [127:0] WDATA
   ,input  [15:0]  WSTRB
   ,input          WLAST
   ,input          WVALID
   ,output         WREADY
   ,output [7:0]   BID
   ,output [1:0]   BRESP
   ,output         BVALID
   ,input          BREADY
   ,output [7:0]   RID
   ,output [127:0] RDATA
   ,output [1:0]   RRESP
   ,output         RLAST
   ,output         RVALID
   ,input          RREADY
);
endinterface
