def eat_space(value, eat):
  # print(value, len(value))
  st = 0
  LEN = len(value)
  ed = LEN - 1
  while st < LEN and eat.find(value[st]) != -1:
    st += 1
  while ed >= 0 and eat.find(value[ed]) != -1:
    ed -= 1
  return value[st:ed+1]