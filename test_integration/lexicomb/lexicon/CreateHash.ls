{
  hash := {};
  key_index := 0;
  value_index := 1;

  key := ReturnNothing _;
  value := ReturnNothing _;

  @?[args[key_index]] && [args[value_index]] {
    key := args[key_index];
    hash[key] := args[value_index];
    key_index := value_index + 1;
    value_index := key_index + 1;
  };

  return hash;
}
