module top(
     input clk

    // comm
         /* vai-auto-port-begin */
        ,input          iCLK
        ,input          iRST
        ,input  [247:0] my_led_addr2
        ,inout          my_led_test1
         /* vai-auto-port-end */
    //end

);

wire xxx_a;
 // start
  /* vai-auto-wire-begin */
  wire [15:0]  my_led_din         ;
  wire [3:0]   my_led_dinx        ;
  wire [7:0]   my_led_LED         ;
  wire [63:0]  my_led_addr1       ;
  wire [7:0]   my_led_strb        ;
  wire         prefix_RST_X_suffix;
  /* vai-auto-wire-end */
  //end


    // example
    led #(
         .STEP  (16   )
        ,.LEN   (8'h1f)
        ,.WIDTH (4'h8 )
    ) u_my_led ( /* vai-auto-inst */
         .CLK   (iCLK               ) //PI
        ,.RST   (iRST               ) //PI
        ,.din   (my_led_din[15:0]   ) //WI
        ,.dinx  (my_led_dinx[3:0]   ) //WO
        ,.LED   (my_led_LED[7:0]    ) //WO
        ,.addr1 (my_led_addr1[63:0] ) //WI
        ,.addr2 (my_led_addr2[247:0]) //PI
        ,.strb  (my_led_strb[3:0]   ) //WO
        ,.test1 (my_led_test1       ) //PIO
    ); // end of u_my_led

TOP u_top ( /* vai-auto-inst */
     .CLK   (iCLK                  ) //PI
    ,.RST_X (prefix_RST_X_suffix   ) //WI
    ,.IN    (my_led_strb[7:0]      ) //WI
    ,.OUT   (my_led_addr2[7:0]) //PO
); // end of u_top

 
endmodule

// vai-files  : ./macros.v, ./led.v
// vai-incdirs: ../../..
