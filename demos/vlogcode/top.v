module top(
     input clk,
     input rst
    /* vai-autoport-begin */
    ,input          CLK_suffix
    ,input          RST_X_suffix
    ,input  [7:0]   IN_suffix
    ,output [7:0]   OUT_suffix
    /* vai-autoport-end */

);

  wire xxx_a;
  /* vai-autowire-begin */
  wire         prefix_CLK  ;
  wire         prefix_RST  ;
  wire [9:0]   prefix_din  ;
  wire [3:0]   prefix_dinx ;
  wire [7:0]   prefix_LED  ;
  wire [39:0]  prefix_addr1;
  wire [394:0] prefix_addr2;
  wire [3:0]   prefix_strb ;
  wire         prefix_test1;
  /* vai-autowire-end */


    // example
    led #(
         .STEP  (10   )
        ,.LEN   (8'h4f)
        ,.WIDTH (4'h8 )
    ) u_my_led ( /* vai-autoinst */
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

    TOP u_top ( /* vai-autoinst */
         .CLK   (CLK_suffix     ) //PI
        ,.RST_X (RST_X_suffix   ) //PI
        ,.IN    (IN_suffix[7:0] ) //PI
        ,.OUT   (OUT_suffix[7:0]) //PO
    ); // end of u_top

 
endmodule

// vai-incfiles: ./macros.v, ./led.v
// vai-incdirs: ./submod
