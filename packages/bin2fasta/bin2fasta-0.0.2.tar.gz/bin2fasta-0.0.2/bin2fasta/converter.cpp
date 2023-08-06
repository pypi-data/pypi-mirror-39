/*cppimport
<%
setup_pybind11(cfg)
%>
*/

#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(converter, m) {
    m.def("add", &add, "A function which adds two numbers");
}
