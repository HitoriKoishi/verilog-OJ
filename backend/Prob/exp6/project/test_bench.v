`timescale 1ns/1ps

module test_bench();
    // 时钟和复位信号定义
    reg clk;
    reg rstn;
    wire [3:0] your_out, ref_out;
    
    // 错误检测信号
    wire mismatch = (ref_out !== your_out);
    reg has_mismatch = 0;
    reg test_failed = 0;
    
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
        rstn = 0;  // 复位有效
        #20;
        
        // 测试用例1：复位测试
        $display("Test 1: Reset test");
        has_mismatch = 0;
        // 释放复位
        rstn = 1;
        #10;
        
        // 测试用例2：计数测试（0->9）
<<<<<<< HEAD
        $display("Test 2: Count test (0->9)");
        repeat(10) #10 has_mismatch = 0;
=======
        repeat(9) begin
            if (your_out !== ref_out) begin
                $display("TEST FAILED");
                $display("Count test failed at value %d!", ref_out);
                $display("Expected output: %b", ref_out);
                $display("Actual output: %b", your_out);
                $finish;
            end
            #10;
        end
>>>>>>> a5808a0 (fix: 修复题目模型名与test_bench中的不匹配的问题)
        
        // 测试用例3：溢出测试（9->0）
        $display("Test 3: Overflow test (9->0)");
        has_mismatch = 0;
        
        // 测试用例4：连续计数测试
        $display("Test 4: Continuous count test (0->9)");
        repeat(20) #10 has_mismatch = 0;
        
        // 测试用例5：异步复位测试
        $display("Test 5: Async reset test");
        #3 rstn = 0;  // 在时钟周期中间复位
        #2 has_mismatch = 0;

        $display("\n=== Simulation Summary ===");
        if (test_failed) begin
            $display("** x TEST FAILED! x **");
        end else begin
            $display("** √ TEST PASSED! √ **");
            $display("No mismatches detected");
        end
        $display("Simulation time: %0t ps", $time);
        $display("========================");
        $finish();
    end
    
    // 错误检测
    always @(*) begin
        if (mismatch && !has_mismatch) begin
            has_mismatch = 1;
            test_failed = 1;
            $display("ERROR: Detect mismatch at time %d", $time);
            $display("Expected output: %b", ref_out);
            $display("Actual output: %b", your_out);
        end
    end
    
    // 实例化待测试模块
    decimal_counter user_module(
        .clk(clk),
        .rstn(rstn),
        .count(your_out)
    );
    
    // 实例化参考模块
    ref_module ref_module(
        .clk(clk),
        .rstn(rstn),
        .count(ref_out)
    );
    
endmodule