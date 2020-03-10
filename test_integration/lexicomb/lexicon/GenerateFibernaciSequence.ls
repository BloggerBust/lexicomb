{
  end := arg0;
  position := 0;
  sequence := {};

  ?[arg1] {
    position := arg1;
  };

  ?[arg2] {
    sequence := arg2;
  };

  ? position = 0 {
    sequence[position] := 0;
    position := position + 1;
    sequence := GenerateFibernaciSequence end position sequence;
  }
  ? position = 1 {
    sequence[position] := 1;
    position := position + 1;
    sequence := GenerateFibernaciSequence end position sequence;
  }
  ? position <= end {
    position_minus_1 := position - 1;
    position_minus_2 := position - 2;

    sequence[position] := sequence[position_minus_1] + sequence[position_minus_2];
    position := position + 1;
    sequence := GenerateFibernaciSequence end position sequence;
  }

  return sequence;
}
