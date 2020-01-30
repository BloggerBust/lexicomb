{
    count := 0;
    @?[args[count]]{
      ?[words]{
        words := words + args[count];
      }
      {
        words := args[count];
      }
      count := count + 1;
    };
    return words;
}
