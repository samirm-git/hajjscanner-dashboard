import math

def get_bin_edges(array: list[float] | list[int], guess_lb: int, guess_ub: int, step: int) -> list[int]:
  
  ppp_lb = math.floor(min(array) / step) * step
  ppp_ub = math.ceil(max(array) / step) * step

  if ppp_lb >= guess_lb:
     if ppp_ub <= guess_ub:
        return list(range(ppp_lb, ppp_ub, step))
     else:
        return list(range(ppp_lb, guess_ub, step)) + [ppp_ub] #extra outlier bin for unexpectedly large values 
  else:
      if ppp_ub <= guess_ub:
        return [ppp_lb] + list(range(guess_lb, ppp_ub, step)) #extra outlier bin for unexpectedly small values
      else:
        return [ppp_lb] + list(range(guess_lb, guess_ub, step)) + [ppp_ub] #extra outlier bins for both cases