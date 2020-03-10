{
  count := 0;
  blank := ReturnNothing _;
  @?[args[count]]{
    ?[words]{
      words := words + blank + args[count];
    }
    {
      words := args[count];
    }
    count := count + 1;
  };
  return words;
}
