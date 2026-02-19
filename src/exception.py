import sys



def error_message_detail(error,error_detail:sys):
    #exceution info it will tell about 3 parameters
    #we need exc_tb parameter
   _,_,exc_tb= error_detail.exc_info()
   file_name=exc_tb.tb_frame.f_code.co_filename #to get file name
   error_message="Error occured in python script name [{0}] line number [{1}] error message  [{2}]".format(
      

       file_name,
       exc_tb.tb_lineno,
       str(error)) #3 parameters

  return error_message

  


class CustomException(Exception):
   
   def __init__(self,error_message,error_detail:sys):
      super().__init__(error_message)
      self.error_message=error_message_detail(error_message,error_detail=error_detail)


    def __str__(self):
      return self.error_message