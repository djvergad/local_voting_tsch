#!/bin/bash

grep -oP 'steady/\Ksteady[^)]*' README.md | \
  while IFS= read -r path
  do
    labeltext="${path#steady_}"
    labeltext="${labeltext%_vs_*}"
    labeltext="${labeltext//_/\\_}"
    label="${path%.png}"
    cat <<- EOF
			\begin{figure}
			  \centering
			  \includegraphics[width=0.9\textwidth]{{{$label}}}
			  %\vspace{-0.1cm}
			  \caption{$labeltext.}
			  %\vspace{-0.5cm}
			  \label{$label}
			\end{figure}

		EOF
  done
