import regex
test_case ='''
   	@yahoo.com 
   	@hotmail.com 	
 	@aol.com 	
 	@gmail.com 	
 	@msn.com 	
 	@comcast.net 	
 	@hotmail.co.uk 	
 	@sbcglobal.net 	
 	@yahoo.co.uk 	
 	@yahoo.co.in 	
 	@bellsouth.net 	
 	@verizon.net 	
 	@earthlink.net 	
 	@cox.net 	
 	@rediffmail.com 	
 	@yahoo.ca 	
 	@btinternet.com 	
 	@charter.net 	
 	@shaw.ca 	
    @ntlworld.com 	
  	'''
def check(mail_id):
	after=regex.compile(mail_id[mail_id.index('@'):])
	matches=after.findall(test_case)
	if matches!=[]:
		return True
	else:
		return False
