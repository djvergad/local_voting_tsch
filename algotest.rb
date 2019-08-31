#!/usr/bin/env ruby

network = {
  1 => 2,
  2 => 0,
  3 => 0,
  4 => 0,
  5 => 4
}

queue = {
  1 => 100,
  2 => 100,
  3 => 100,
  4 => 100,
  5 => 100
}

channels = 1
timeslots = 30
weight = network.keys.product(network.keys).map do |k1,k2|
  if k1 == k2 || network[k1] == k2 || network[k2] == k1
    [[k1,k2], 1.0 ]
  else
    [[k1,k2], 0 ]
  end
end.to_h
p weight


i = 0
while queue.values.max > 0 do
  q2 = {}
  network.each do |s,d|
    while s != 0 
      q2[s] ||= 0
      q2[s] += queue[s]
      s = network[s]
      d = network[d]
    end
  end

#  def calc_q2(n)
#    q2[n] ||= 0
#    q2[n] += queue[n]
#    calc_q2(network[n]) unless network[n] == 0
#  end
#  network.keys.each do |n|
#    calc_q2(n)
#  end

  p "q2 = #{q2}"
  slots = q2.map do |node,q|
    q_sum = q2.sum do |other, q_other|
      weight[[node,other]] * q_other
    end
    [node, q > 0 ? (q / q_sum * timeslots).round: 0]
  end.to_h
 
  newpkts = (1..5).map { |i| [i, 0] }.to_h
  network.each do |k,v|
    newpkts[v] = [slots[k], queue[k]].min
  end

  queue = queue.map do | node,q |
    [node, [q-slots[node] + newpkts[node],0].max]
  end.to_h
  i+=1
  puts "#{i}: The queue is #{queue}, p_sum is #{slots.values.sum}"
end
