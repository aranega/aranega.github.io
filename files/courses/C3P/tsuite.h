#include <check.h>
#include <stdarg.h>

void add2tsuite(TCase *, int, ...);
#define ADD2TSUITE(s, ...) add2tsuite(s, sizeof((TFun []) {__VA_ARGS__}) / sizeof(TFun), __VA_ARGS__)

void add2tsuite(TCase * core, int n, ...) {
  int i;
  va_list va;
  va_start(va, n);
  for (i = 0; i < n; i++) {
    tcase_add_test(core, va_arg(va, TFun));
  }
  va_end(va);
}


#define TSUITE(Tlabel, Tname, ...) Suite * Tlabel(void) \
{ \
  Suite *s = suite_create(Tname); \
  TCase *tc_core = tcase_create("Core"); \
  ADD2TSUITE(tc_core, __VA_ARGS__); \
  suite_add_tcase(s, tc_core); \
  return s; \
}

typedef Suite * (* CSFun)(void);

void add_suites(SRunner *, int, ...);
#define ADD_SUITES(sr, ...) add_suites(sr, (sizeof((CSFun []) {__VA_ARGS__}) / sizeof(CSFun)), __VA_ARGS__)
void add_suites(SRunner *sr, int n, ...) {
  int i;
  va_list va;
  va_start(va, n);
  for (i = 0; i < n; i++) {
    Suite * (*sfun)(void) = va_arg(va, CSFun);
    srunner_add_suite(sr, sfun());
  }
  va_end(va);
}

#define _RUN_SINGLE(Tlabel) int main(void) \
{ \
  int number_failed; \
  Suite * s = Tlabel(); \
  SRunner * sr = srunner_create(s); \
  srunner_run_all(sr, CK_NORMAL); \
  number_failed = srunner_ntests_failed(sr); \
  srunner_free(sr); \
  return (number_failed == 0) ? 0 : 1; \
}


#define _RUN_ALL(Tlabel, ...) int main(void) \
{ \
  int number_failed; \
  Suite * s = Tlabel(); \
  SRunner * sr = srunner_create(s); \
  ADD_SUITES(sr, __VA_ARGS__); \
  srunner_run_all(sr, CK_NORMAL); \
  number_failed = srunner_ntests_failed(sr); \
  srunner_free(sr); \
  return (number_failed == 0) ? 0 : 1; \
}

#define _RUN_OVERRIDE(_1, _2, NAME, ...)   NAME
#define RUN_ALL(...)                       _RUN_OVERRIDE(__VA_ARGS__, _RUN_ALL, _RUN_SINGLE)(__VA_ARGS__)
