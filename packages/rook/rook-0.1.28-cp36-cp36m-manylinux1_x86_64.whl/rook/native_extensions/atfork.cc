#include "common.h"
#include "atfork.h"

#include <pthread.h>
#include <stdio.h>

namespace native_extensions {

// Global variable to know if we already printed the messgae
int g_python_fork_handler_called = 0;

// The actual callback that is called before the forking
static void preforkCallback() {
  if (!g_python_fork_handler_called) {
    printf("[Rookout] Rookout does not support running in forking processes. Please import only after forking.\n");
    g_python_fork_handler_called = 1;
  }
}

// Python callback that registers to the pre-forking notification
PyObject* RegisterPreforkCallback(PyObject* self, PyObject* py_args) {
  if (pthread_atfork(preforkCallback, NULL, NULL)) {
    Py_RETURN_TRUE;
  } else {
    Py_RETURN_FALSE;
  }
}

}  // namespace native_extensions

