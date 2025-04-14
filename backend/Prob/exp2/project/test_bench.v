`timescale 1ns/1ps

module test_bench();
    // 信号定义
    reg a, b, c;
    wire your_out, ref_out;
    
    // 错误检测信号
    wire mismatch = (ref_out !== your_out);
    reg has_mismatch = 0;
    reg [63:0] first_mismatch_time = -1;
    
    // 波形生成
    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars(0, test_bench);
    end
    
    // 测试激励
    initial begin
        // 测试所有输入组合
        a = 0; b = 0; c = 0; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 000 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 0; b = 0; c = 1; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 001 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 0; b = 1; c = 0; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 010 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 0; b = 1; c = 1; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 011 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 1; b = 0; c = 0; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 100 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 1; b = 0; c = 1; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 101 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 1; b = 1; c = 0; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 110 failed!");
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
            $finish;
        end
        
        a = 1; b = 1; c = 1; #10;
        if (your_out !== ref_out) begin
            $display("TEST FAILED");
            $display("Test case 111 failed!");
            $display("Expected output: %b", ref_out);
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
    nand3_gate user_module(
        .a(a),
        .b(b),
        .c(c),
        .y(your_out)
    );
    
    // 实例化参考模块
    ref_module ref_module(
        .a(a),
        .b(b),
        .c(c),
        .y(ref_out)
    );
    
endmodule