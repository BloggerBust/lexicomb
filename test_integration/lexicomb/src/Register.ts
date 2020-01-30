{
    registrant_first_name := arg0;
    ? [arg1] {
      registrant_last_name := arg1;
    };

    result := {};
    result[registrant_first_name] := {};
    return result;
}
