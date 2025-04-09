`timescale 1ns/1ps

module testbench;
  reg a, b, cin;
  wire sum, cout;
  
  // 引用提交的模块
  solution uut(
    .a(a),
    .b(b),
    .cin(cin),
    .sum(sum),
    .cout(cout)
  );
  
  initial begin
    // 测试用例
    a = 0; b = 0; cin = 0; #10;
    if (sum !== 0 || cout !== 0) $display("错误: a=0,b=0,cin=0");
    
    a = 0; b = 0; cin = 1; #10;
    if (sum !== 1 || cout !== 0) $display("错误: a=0,b=0,cin=1");
    
    a = 0; b = 1; cin = 0; #10;
    if (sum !== 1 || cout !== 0) $display("错误: a=0,b=1,cin=0");
    
    a = 0; b = 1; cin = 1; #10;
    if (sum !== 0 || cout !== 1) $display("错误: a=0,b=1,cin=1");
    
    a = 1; b = 0; cin = 0; #10;
    if (sum !== 1 || cout !== 0) $display("错误: a=1,b=0,cin=0");
    
    a = 1; b = 0; cin = 1; #10;
    if (sum !== 0 || cout !== 1) $display("错误: a=1,b=0,cin=1");
    
    a = 1; b = 1; cin = 0; #10;
    if (sum !== 0 || cout !== 1) $display("错误: a=1,b=1,cin=0");
    
    a = 1; b = 1; cin = 1; #10;
    if (sum !== 1 || cout !== 1) $display("错误: a=1,b=1,cin=1");
    
    $display("Test passed: all cases correct");
    $finish;
  end
endmodule
