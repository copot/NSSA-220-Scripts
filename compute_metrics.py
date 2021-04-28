def compute(parsedData) :
	print('called compute function in compute_metrics.py')
	fCSV = open("Project2Output.csv", 'w')
	fCSV.truncate(0)
	fCSV.close()
	nodeIP = ["100.1", "100.2", "200.1", "200.2"] #IP endings used to determine if packet is recieved or sent
	for filenum in range(0, 4) :
		ERS = 0 #Echo req Sent
		ERR = 0 #echo req recieved
		EReS = 0 #echo reply sent
		EReR = 0 #echo reply recieved
		ERSacc = 0 #ERS acc
		ERRacc = 0 #ERR acc
		EReSacc = 0 #EReS acc
		EReRacc = 0 #EReR acc
		ERRgoodACC = 0
        
		ERThrough = 0 #Echo request Throughput
		ERGood = 0 #Echo request Goodput
        
		RTT = 0 # RTT
		total = 0 # Accumulate echo request time data for RTT calculation
		count1 = 0 # Accumulate echo request total number for RTT calc
		time = 0 # Placeholder for packet time to be stored to other locations
		reqTime = 0 # source echo request time
		repTime = 0 # Holds packet reply time to RTT calculation

		hop = 0 # Total hop data count for hop average calculation
		requestcount = 0 # Total hop run count for average calculation
		avgHop = 0 # Holds average hop calculation
        
		gate = 0 # Terrible gate to add totals because getting the times is a mess since it's gotten one at a time
        
		avgDelayReply = 0 # holds the average reply delay calculation
		count2 = 0 # Accumulator for average reply delay caclulation
		total2 = 0 # Total data for average reply delay calculation
        
		for icmpPacket in parsedData[filenum] :
			source = icmpPacket[0]
			dest = icmpPacket[1]
			size = icmpPacket[2]
			icmpType = icmpPacket[3]
			time = float(icmpPacket[4])
			ttl = icmpPacket[5]
			ttl = ttl[4:]
			ttl = int(ttl)
			curip = "192.168." + nodeIP[filenum] #Current node IP

			if "request" == icmpType :
				if source == curip :
					ERS = ERS + 1
					ERSacc = ERSacc + int(size)
					ERRgoodACC = ERRgoodACC + int(size) - 42
					reqTime = time

				elif dest == curip :
					ERR = ERR + 1
					ERRacc = ERRacc + int(size)
					
					recTime = time
                
				requestcount = requestcount + 1
                
			elif "reply" == icmpType :
				if source == curip :
					EReS = EReS + 1
					EReSacc = EReSacc + int(size) - 42
                    
					recRepTime = time # 
					gate = 2

				elif dest == curip :
					EReR = EReR + 1
					EReRacc = EReRacc + int(size) - 42
					repTime = time
					gate = 1
					hop = hop + (129 - ttl) # Should record hop counts for requests
                
                # Should get the times and add to totals depending on the IP of reply 
			if gate == 1 : # For RTT
				total = total + (repTime - reqTime) # RTT is node sending request. Reply recieve time - request send time
				count1 = count1 + 1

			elif gate == 2 : # For average reply delay
				total2 = total2 + (recRepTime - recTime) # Reply delay is node recieving request. Reply send time - request get time
				count2 = count2 + 1

			gate = 0 
                     
		RTT = round((((total) / count1) * 1000), 2)                # RTT total
		ERThrough = round(((ERSacc / total)  / 1000), 1)          # Should be Echo request throughput number
		ERGood = round(((ERRgoodACC / total) / 1000), 1)              # Should be Echo request goodput number
		avgDelayReply = round(((total2 / count2) * 1000000), 2)     # Average delay reply          
		avgHop = round((hop / ERS),2)          # average hop count
                    
		writetoCSV([str(filenum + 1), str(ERS), str(ERR), str(EReS), str(EReR), str(ERSacc), str(EReRacc), str(ERRacc), str(EReSacc), str(RTT), str(ERThrough), str(ERGood), str(avgDelayReply), str(avgHop)])
		print("Node" + str(filenum + 1) + " computed.")
	print("Parsed packet captures computed.")

def writetoCSV(data) :
	fCSV = open("Project2Output.csv", 'a')
	fCSV.write("Node " + data[0] + "\n")
	fCSV.write("\n")
	fCSV.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received" + "\n")
	fCSV.write(data[1] + "," + data[2] + "," + data[3] + "," + data[4] + "\n")
	fCSV.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)" + "\n")
	fCSV.write(data[5] + "," + data[6] + "\n")
	fCSV.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)" + "\n")
	fCSV.write(data[7] + "," + data[8] + "\n\n")
	fCSV.write("Average RTT (miliseconds)" + "\n")
	fCSV.write(data[9] + "\n")
	fCSV.write("Echo Request Throughput (kB/sec)" + "\n")
	fCSV.write(data[10] + "\n")
	fCSV.write("Echo Request Goodput (kB/sec)" + "\n")
	fCSV.write(data[11] + "\n")
	fCSV.write("Average Reply Delay" + "\n")
	fCSV.write(data[12] + "\n")
	fCSV.write("\n")
	fCSV.write("Average Echo Request Hop Count" + "\n")
	fCSV.write(data[13] + "\n")
	fCSV.write("\n")
	fCSV.close()
