// `include "macros.v"
`define ADDR 4
module led #
  (
   parameter STEP = 10,
             LEN = 8'h4f
   )
  (
   input CLK,
   input RST,
   input [STEP-1:0] din,
   output [`ADDR-1:0] dinx,
   output reg [7:0] LED,
   input [(`ADDR*STEP-1):0] addr1,
   input [(LEN*STEP >> 1)-1:0] addr2,
   output [`SIZE/8-1:0] strb,
   inout test1
   );
  
parameter WIDTH = 4'h8;
localparam DEPTH = 16;

  reg [31:0] count;
  
  always @(posedge CLK) begin
    if(RST) begin
      count <= 0;
      LED <= 0;
    end else begin
      if(count == STEP - 1) begin
        count <= 0;
        LED <= LED + 1;
      end else begin
        count <= count + 1;
      end
    end
  end
endmodule

/*
module ledx #
  (
   parameter STEP = 10,
             LEN = 8'h4f
   )
  (
   input CLK,
   input RST,
   input [STEP-1:0] din,
   output [`ADDR-1:0] dinx,
   output reg [7:0] LED,
   input [(`ADDR*STEP-1):0] addr1,
   input [(LEN*STEP >> 1)-1:0] addr2,
   inout test1
   );
  
parameter WIDTH = 4'h8;
localparam DEPTH = 16;

  reg [31:0] count;
  
  always @(posedge CLK) begin
    if(RST) begin
      count <= 0;
      LED <= 0;
    end else begin
      if(count == STEP - 1) begin
        count <= 0;
        LED <= LED + 1;
      end else begin
        count <= count + 1;
      end
    end
  end
endmodule
*/