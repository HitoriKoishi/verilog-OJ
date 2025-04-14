`timescale 1ns/1ps

module test_bench();
	// 时钟和复位信号定义
	reg clk;
	reg rst;
	reg j, k;
	wire your_out, ref_out;
	
	// 错误检测信号
	wire mismatch = (ref_out !== your_out);
	reg has_mismatch = 0;
	reg [63:0] first_mismatch_time = -1;
	
	// 时钟生成
	initial begin
		clk = 0;
		forever #5 clk = ~clk;
	end
	
	// 波形生成
	initial begin
		$dumpfile("waveform.vcd");
		$dumpvars(0, test_bench);
	end
	
	// 测试激励
	initial begin
		// 初始化
		rst = 1;  // 复位有效
		j = 0;
		k = 0;
		#20;
		
		// 测试用例1：复位测试
		if (your_out !== 1'b0) begin
			$display("TEST FAILED");
			$display("Reset test failed!");
			$display("Expected output: 0");
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 释放复位
		rst = 0;
		#20;
		
		// 测试用例2：保持状态(J=0,K=0)
		j = 0; k = 0;
		#10;
		if (your_out !== ref_out) begin
			$display("TEST FAILED");
			$display("Hold state test failed!");
			$display("Expected output: %b", ref_out);
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 测试用例3：置1(J=1,K=0)
		j = 1; k = 0;
		#10;
		if (your_out !== ref_out) begin
			$display("TEST FAILED");
			$display("Set test failed!");
			$display("Expected output: %b", ref_out);
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 测试用例4：置0(J=0,K=1)
		j = 0; k = 1;
		#10;
		if (your_out !== ref_out) begin
			$display("TEST FAILED");
			$display("Reset test failed!");
			$display("Expected output: %b", ref_out);
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 测试用例5：翻转(J=1,K=1)
		j = 1; k = 1;
		#10;
		if (your_out !== ref_out) begin
			$display("TEST FAILED");
			$display("Toggle test failed!");
			$display("Expected output: %b", ref_out);
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 测试用例6：再次翻转(J=1,K=1)
		#10;
		if (your_out !== ref_out) begin
			$display("TEST FAILED");
			$display("Second toggle test failed!");
			$display("Expected output: %b", ref_out);
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 测试用例7：异步复位测试
		#5 rst = 1;  // 在时钟周期中间复位
		#2;
		if (your_out !== 1'b0) begin
			$display("TEST FAILED");
			$display("Async reset test failed!");
			$display("Expected output: 0");
			$display("Actual output: %b", your_out);
			$finish;
		end
		
		// 所有测试通过
		$display("TEST PASSED");
		$display("All test cases passed!");
		$finish;
	end
	
	// 超时保护
	initial begin
		#1000;
		$display("TEST FAILED");
		$display("Simulation timeout!");
		$finish;
	end
	
	// 错误检测
	always @(*) begin
		if (mismatch && !has_mismatch) begin
			has_mismatch = 1;
			first_mismatch_time = $time;
		end
	end
	
	// 实例化待测试模块
	jk_ff user_module(
		.clk(clk),
		.rst(rst),
		.j(j),
		.k(k),
		.q(your_out)
	);
	
	// 实例化参考模块
	ref_module ref_module(
		.clk(clk),
		.rst(rst),
		.j(j),
		.k(k),
		.q(ref_out)
	);
	
endmodule