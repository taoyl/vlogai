// AXI4 interface
interface axi4;
    wire         ACLK;
    wire         ARESETn;
    wire [31:0]  AWADDR;
    wire [7:0]   AWID;
    wire         AWVALID;
    wire         AWREADY;
    wire [3:0]   AWSIZE;
    wire [3:0]   AWLEN;
    wire [31:0]  ARADDR;
    wire [7:0]   ARID;
    wire         ARVALID;
    wire         ARREADY;
    wire [3:0]   ARSIZE;
    wire [3:0]   ARLEN;
    wire [127:0] WDATA;
    wire [15:0]  WSTRB;
    wire         WLAST;
    wire         WVALID;
    wire         WREADY;
    wire [7:0]   BID;
    wire [1:0]   BRESP;
    wire         BVALID;
    wire         BREADY;
    wire [7:0]   RID;
    wire [127:0] RDATA;
    wire [1:0]   RRESP;
    wire         RLAST;
    wire         RVALID;
    wire         RREADY;

    modport slave(
         input  ACLK
        ,input  ARESETn
        ,input  AWADDR
        ,input  AWID
        ,input  AWVALID
        ,output AWREADY
        ,input  AWSIZE
        ,input  AWLEN
        ,input  ARADDR
        ,input  ARID
        ,input  ARVALID
        ,output ARREADY
        ,input  ARSIZE
        ,input  ARLEN
        ,input  WDATA
        ,input  WSTRB
        ,input  WLAST
        ,input  WVALID
        ,output WREADY
        ,output BID
        ,output BRESP
        ,output BVALID
        ,input  BREADY
        ,output RID
        ,output RDATA
        ,output RRESP
        ,output RLAST
        ,output RVALID
        ,input  RREADY
    );

    modport master(
         output  ACLK
        ,output  ARESETn
        ,output  AWADDR
        ,output  AWID
        ,output  AWVALID
        ,input   AWREADY
        ,output  AWSIZE
        ,output  AWLEN
        ,output  ARADDR
        ,output  ARID
        ,output  ARVALID
        ,input   ARREADY
        ,output  ARSIZE
        ,output  ARLEN
        ,output  WDATA
        ,output  WSTRB
        ,output  WLAST
        ,output  WVALID
        ,input   WREADY
        ,input   BID
        ,input   BRESP
        ,input   BVALID
        ,output  BREADY
        ,input   RID
        ,input   RDATA
        ,input   RRESP
        ,input   RLAST
        ,input   RVALID
        ,output  RREADY
    );
    
endinterface : axi4
