<<<<<<< HEAD

=======
>>>>>>> a5808a0 (fix: 修复题目模型名与test_bench中的不匹配的问题)
module decimal_counter(
    input clk,
    input rstn,
    output [3:0] count
    );
    reg [3:0] q;
    assign count = q;

endmodule