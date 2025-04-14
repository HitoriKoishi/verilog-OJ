`timescale 1ns/1ps

module test_bench();
    // 时钟和复位信号定义
    reg clk;
    reg rst;
    wire [3:0] your_out, ref_out;
    
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
        rst = 0;  // 复位有效
        #20;
        
        // 测试用例1：复位测试
        if (your_out !== 4'b0000) begin
            $display("TEST FAILED");
            $display("Reset test failed!");
            $display("Expected output: 0000");
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 释放复位
        rst = 1;
        #10;
        
        // 测试用例2：计数测试（0->9）
        repeat(10) begin
            if (your_out !== ref_out) begin
                $display("TEST FAILED");
                $display("Count test failed at value %d!", ref_out);
                $display("Expected output: %b", ref_out);
                $display("Actual output: %b", your_out);
                $finish;
            end
            #10;
        end
        
        // 测试用例3：溢出测试（9->0）
        if (your_out !== 4'b0000) begin
            $display("TEST FAILED");
            $display("Overflow test failed!");
            $display("Expected output: 0000");
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 测试用例4：连续计数测试
        repeat(20) begin
            if (your_out !== ref_out) begin
                $display("TEST FAILED");
                $display("Continuous count test failed!");
                $display("Expected output: %b", ref_out);
                $display("Actual output: %b", your_out);
                $finish;
            end
            #10;
        end
        
        // 测试用例5：异步复位测试
        #3 rst = 0;  // 在时钟周期中间复位
        #2;
        if (your_out !== 4'b0000) begin
            $display("TEST FAILED");
            $display("Async reset test failed!");
            $display("Expected output: 0000");
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
        #2000;
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
    decimal_counter user_module(
        .clk(clk),
        .rst(rst),
        .count(your_out)
    );
    
    // 实例化参考模块
    ref_module ref_module(
        .clk(clk),
        .rst(rst),
        .count(ref_out)
    );
    
endmodule