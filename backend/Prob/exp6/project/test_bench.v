`timescale 1ns / 1ps
module test_bench();
    
    reg rst;
    reg clk;
    wire [3:0] count;
    
    counter_10 counter_10(.clk(clk),.rst(rst), .count(count));
     
    initial 
    begin
      rst <= 0;
      clk <= 0;
      #50 rst <= 1;
      #2000 rst <= 0;
    end
    always
      #10 clk = ~clk;

endmodule