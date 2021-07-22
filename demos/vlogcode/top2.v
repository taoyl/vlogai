module top2(
     input clk,
     input rst
);

  wire xxx_a;
  wire refclk;
  wire rstn = ~rst;

    // example
    example_mod u_example_mod ( /* vai-autoinst */
         .ref_clk(refclk)
        ,.sys_rstn(rstn)
        ,.cpucore_mst(cpu_core1_mst) //WO
        ,.syscsr_slv(sys_csr0_slv) //WI
    );

 
endmodule

// vai-incifflists: ./interface/iflib.flist
// vai-incifs: ./interface/example_mod.if.sv
// vai-incdirs: ./submod
