module top(
     input clk,
     input rst,
     output [3:0] dbg1,
     output [6*4-1:0] dbg2,
     output [(16<<2)/2-1:0] dbg3
);

  wire xxx_a;

    // example
    led u_my_led ( /* vai-autoinst */
    ); // end of u_my_led

    TOP u_top ( /* vai-autoinst */
    ); // end of u_top

 
endmodule

// vai-incfiles: ./macros.v, ./led.v
// vai-incdirs: ./submod
