`timescale 1ns/1ps

module test_bench();
    // 时钟和复位信号定义
    reg clk;
    reg rstn;
    reg in;
    wire your_out, ref_out;
    
    // 错误检测信号
    wire mismatch = (ref_out !== your_out);
    reg has_mismatch = 0;
    reg [63:0] first_mismatch_time = -1;
    
    // 时钟生成
    initial begin
        clk = 0;
        forever #10 clk = ~clk;
    end
    
    // 波形生成
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, test_bench);
    end
    
    // 测试激励
    initial begin
        // 初始化
        rstn = 1;
        in = 0;
        #30;
        
        // 测试用例1：复位测试
        rstn = 0;
        #50;
        if (your_out !== 1'b0) begin
            $display("TEST FAILED");
            $display("Reset test failed!");
            $display("Expected output: 0");
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        // 释放复位
        rstn = 1;
        #20;
        
        // 测试用例2：功能测试
        // 测试序列：0->1->0->1->0
        in = 1'b1;
        #25;
        in = 1'b0;
        #25;
        in = 1'b1;
        #25;
        in = 1'b0;
        #25;
        
        // 检查是否有不匹配
        if (has_mismatch) begin
            $display("TEST FAILED");
            $display("First mismatch occurred at %0t ps", first_mismatch_time);
            $finish;
        end
        
        // 所有测试通过
        $display("TEST PASSED");
        $display("All test cases passed!");
        $finish;
    end
    
    // 超时保护
    initial begin
        #10000;
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
    xor_trigger user_module(
        .clk    (clk),
        .rstn   (rstn),
        .in     (in),
        .out    (your_out)
    );
    
    // 实例化参考模块
    ref_module ref_module(
        .clk    (clk),
        .rstn   (rstn),
        .in     (in),
        .out    (ref_out)
    );
    
endmodule
