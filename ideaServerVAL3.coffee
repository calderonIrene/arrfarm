begin
  putln("Server program is starting")
  while(true)
    // Read data form TCP server socket
    sioGet(io:receive_joints, to_receive)


   
    put(to_receive[i])  
   
    // Decodify the 24 bytes read into 6 floats with 4 bytes each, big-endian
    fromBinary(to_receive, 24, "4.0b", joint_states_cm)
    // Fill a jointRX var
    j_move.j1 = joint_states_cm[0]
    j_move.j2 = joint_states_cm[1]
    j_move.j3 = joint_states_cm[2]
    j_move.j4 = joint_states_cm[3]
    j_move.j5 = joint_states_cm[4]
    j_move.j6 = joint_states_cm[5]
   
    // Move the arm to the received position
    movej(j_move, flange, mNomSpeed)
  endWhile
end



# while true: // estem sempre escoltant
  # Llegim la primera dada (corresponent al tipus) DATA1

    # if DATA1 == "feedback":
      # llegimResposta DATA2
        # if DATA2 == "YES" 
          # baixem cap baix i agafem medicament
        # if DATA2 == "NO"
          # Anem a mirar el seguent codi

    # else if DATA1 == calaix:
      # llegim posició calaix (rebem DATA3)
      # anem a la posició del calatx
      