module top2(
     input clk,
     input rst
  /* vai-autoport-begin */
  /* vai-autoport-end */

);

  wire xxx_a;
  wire refclk;
  wire rstn = ~rst;
  /* vai-autowire-begin */
  /* vai-autowire-end */

    // example
    example_mod u_example_mod ( /* vai-autoinst */
         .ref_clk             (refclk                    ) //I
        ,.sys_rstn            (rstn                      ) //I
        ,.global_cg_enable    (global_cg_enable          ) //WI
        ,.dbg_bus             (dbg_bus[7:0]              ) //WO
        ,.error_fiq           (error_fiq                 ) //WO
        ,.cpucore_mst_ACLK    (cpu_core1_mst_ACLK        ) //WI
        ,.cpucore_mst_ARESETn (cpu_core1_mst_ARESETn     ) //WI
        ,.cpucore_mst_AWADDR  (cpu_core1_mst_AWADDR[31:0]) //WO
        ,.cpucore_mst_AWID    (cpu_core1_mst_AWID[7:0]   ) //WO
        ,.cpucore_mst_AWVALID (cpu_core1_mst_AWVALID     ) //WO
        ,.cpucore_mst_AWREADY (cpu_core1_mst_AWREADY     ) //WI
        ,.cpucore_mst_AWSIZE  (cpu_core1_mst_AWSIZE[3:0] ) //WO
        ,.cpucore_mst_AWLEN   (cpu_core1_mst_AWLEN[3:0]  ) //WO
        ,.cpucore_mst_ARADDR  (cpu_core1_mst_ARADDR[31:0]) //WO
        ,.cpucore_mst_ARID    (cpu_core1_mst_ARID[7:0]   ) //WO
        ,.cpucore_mst_ARVALID (cpu_core1_mst_ARVALID     ) //WO
        ,.cpucore_mst_ARREADY (cpu_core1_mst_ARREADY     ) //WI
        ,.cpucore_mst_ARSIZE  (cpu_core1_mst_ARSIZE[3:0] ) //WO
        ,.cpucore_mst_ARLEN   (cpu_core1_mst_ARLEN[3:0]  ) //WO
        ,.cpucore_mst_WDATA   (cpu_core1_mst_WDATA[127:0]) //WO
        ,.cpucore_mst_WSTRB   (cpu_core1_mst_WSTRB[15:0] ) //WO
        ,.cpucore_mst_WLAST   (cpu_core1_mst_WLAST       ) //WO
        ,.cpucore_mst_WVALID  (cpu_core1_mst_WVALID      ) //WO
        ,.cpucore_mst_WREADY  (cpu_core1_mst_WREADY      ) //WI
        ,.cpucore_mst_BID     (cpu_core1_mst_BID[7:0]    ) //WI
        ,.cpucore_mst_BRESP   (cpu_core1_mst_BRESP[1:0]  ) //WI
        ,.cpucore_mst_BVALID  (cpu_core1_mst_BVALID      ) //WI
        ,.cpucore_mst_BREADY  (cpu_core1_mst_BREADY      ) //WO
        ,.cpucore_mst_RID     (cpu_core1_mst_RID[7:0]    ) //WI
        ,.cpucore_mst_RDATA   (cpu_core1_mst_RDATA[127:0]) //WI
        ,.cpucore_mst_RRESP   (cpu_core1_mst_RRESP[1:0]  ) //WI
        ,.cpucore_mst_RLAST   (cpu_core1_mst_RLAST       ) //WI
        ,.cpucore_mst_RVALID  (cpu_core1_mst_RVALID      ) //WI
        ,.cpucore_mst_RREADY  (cpu_core1_mst_RREADY      ) //WO
        ,.syscsr_slv_ACLK     (sys_csr0_slv_ACLK         ) //WI
        ,.syscsr_slv_ARESETn  (sys_csr0_slv_ARESETn      ) //WI
        ,.syscsr_slv_AWADDR   (sys_csr0_slv_AWADDR[31:0] ) //WI
        ,.syscsr_slv_AWID     (sys_csr0_slv_AWID[7:0]    ) //WI
        ,.syscsr_slv_AWVALID  (sys_csr0_slv_AWVALID      ) //WI
        ,.syscsr_slv_AWREADY  (sys_csr0_slv_AWREADY      ) //WO
        ,.syscsr_slv_AWSIZE   (sys_csr0_slv_AWSIZE[3:0]  ) //WI
        ,.syscsr_slv_AWLEN    (sys_csr0_slv_AWLEN[3:0]   ) //WI
        ,.syscsr_slv_ARADDR   (sys_csr0_slv_ARADDR[31:0] ) //WI
        ,.syscsr_slv_ARID     (sys_csr0_slv_ARID[7:0]    ) //WI
        ,.syscsr_slv_ARVALID  (sys_csr0_slv_ARVALID      ) //WI
        ,.syscsr_slv_ARREADY  (sys_csr0_slv_ARREADY      ) //WO
        ,.syscsr_slv_ARSIZE   (sys_csr0_slv_ARSIZE[3:0]  ) //WI
        ,.syscsr_slv_ARLEN    (sys_csr0_slv_ARLEN[3:0]   ) //WI
        ,.syscsr_slv_WDATA    (sys_csr0_slv_WDATA[127:0] ) //WI
        ,.syscsr_slv_WSTRB    (sys_csr0_slv_WSTRB[15:0]  ) //WI
        ,.syscsr_slv_WLAST    (sys_csr0_slv_WLAST        ) //WI
        ,.syscsr_slv_WVALID   (sys_csr0_slv_WVALID       ) //WI
        ,.syscsr_slv_WREADY   (sys_csr0_slv_WREADY       ) //WO
        ,.syscsr_slv_BID      (sys_csr0_slv_BID[7:0]     ) //WO
        ,.syscsr_slv_BRESP    (sys_csr0_slv_BRESP[1:0]   ) //WO
        ,.syscsr_slv_BVALID   (sys_csr0_slv_BVALID       ) //WO
        ,.syscsr_slv_BREADY   (sys_csr0_slv_BREADY       ) //WI
        ,.syscsr_slv_RID      (sys_csr0_slv_RID[7:0]     ) //WO
        ,.syscsr_slv_RDATA    (sys_csr0_slv_RDATA[127:0] ) //WO
        ,.syscsr_slv_RRESP    (sys_csr0_slv_RRESP[1:0]   ) //WO
        ,.syscsr_slv_RLAST    (sys_csr0_slv_RLAST        ) //WO
        ,.syscsr_slv_RVALID   (sys_csr0_slv_RVALID       ) //WO
        ,.syscsr_slv_RREADY   (sys_csr0_slv_RREADY       ) //WI
    ); // end of u_example_mod

 
endmodule

// vai-incifflists: ./interface/iflib.flist
// vai-incifs: ./interface/example_mod.if.sv
// vai-incdirs: ./submod
