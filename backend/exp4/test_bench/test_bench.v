`timescale 1ns / 1ps
module test_bench();
reg j,k,clk,rst;
wire q;
jk_ff u1(.j(j),.k(k),.clk(clk),.rst(rst),.q(q));
always #5 clk = ~clk;
initial
begin
	rst = 0; clk = 0; j = 1; k = 0;
	#10 j=0;k=0;
	#10 j=1;k=0;
	#10 j=0;k=1;
	#10 j=1;k=1;
	#15	rst = 1;
	#10 j=0;k=0;
	#10 j=1;k=0;
	#10 j=0;k=1;
	#10 j=1;k=1;
end
endmodule