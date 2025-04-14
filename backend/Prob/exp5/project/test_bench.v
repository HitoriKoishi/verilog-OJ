`timescale 1ns/1ps

module test_bench();
    // 时钟和信号定义
    reg clk;
    reg d;
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
        $dumpfile("wave.vcd");
        $dumpvars(0, test_bench);
    end
    
    // 测试激励
    initial begin
        // 初始化
        d = 0;
        #20;
        
        // 测试用例1：输入0
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 1 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 测试用例2：输入1
        d = 1;
        #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 2 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 测试用例3：输入0
        d = 0;
        #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 3 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 测试用例4：快速翻转
        repeat(5) begin
            d = ~d;
            #10;
            if (your_out !== ref_out) begin
                $display("TEST FAILED");
                $display("Fast toggle test failed!");
                $display("Expected output: %b", ref_out);
                $display("Actual output: %b", your_out);
                $finish;
            end
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
    d_ff user_module(
        .clk(clk),
        .d(d),
        .q(your_out)
    );
    
    // 实例化参考模块
    ref_module ref_module(
        .clk(clk),
        .d(d),
        .q(ref_out)
    );
    
endmodule