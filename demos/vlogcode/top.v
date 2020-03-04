module top(
     input clk,
     input rst
             /* vai-auto-port-begin */
             ,input          CLK
             ,input          RST_X
             ,input  [7:0]   IN
             ,output [7:0]   OUT
             /* vai-auto-port-end */

);

wire xxx_a;
 // start
  /* vai-auto-wire-begin */
  wire         CLK  ;
  wire         RST  ;
  wire [9:0]   din  ;
  wire [3:0]   dinx ;
  wire [7:0]   LED  ;
  wire [39:0]  addr1;
  wire [394:0] addr2;
  wire [3:0]   strb ;
  wire         test1;
  /* vai-auto-wire-end */
  //end


    // example
    led #(
         .STEP  (10   )
        ,.LEN   (8'h4f)
        ,.WIDTH (4'h8 )
    ) u_my_led ( /* vai-auto-inst */
         .CLK   (prefix_CLK         ) //WI
        ,.RST   (prefix_RST         ) //WI
        ,.din   (prefix_din[9:0]    ) //WI
        ,.dinx  (prefix_dinx[3:0]   ) //WO
        ,.LED   (prefix_LED[7:0]    ) //WO
        ,.addr1 (prefix_addr1[39:0] ) //WI
        ,.addr2 (prefix_addr2[394:0]) //WI
        ,.strb  (prefix_strb[3:0]   ) //WO
        ,.test1 (prefix_test1       ) //WIO
    ); // end of u_my_led

TOP u_top ( /* vai-auto-inst */
     .CLK   (CLK_suffix     ) //PI
    ,.RST_X (RST_X_suffix   ) //PI
    ,.IN    (IN_suffix[7:0] ) //PI
    ,.OUT   (OUT_suffix[7:0]) //PO
); // end of u_top

 
endmodule

// vai-files  : ./macros.v, ./led.v
// vai-incdirs: ./submod
