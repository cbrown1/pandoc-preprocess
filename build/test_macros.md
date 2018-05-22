---
documentclass: article
fig_caption: {Fig1: 'It describes what Figure 1 shows, and perhaps how to interpret
    it. It may include details of the layout, or note landmarks and other things of
    interest.', Fig2: This caption is different than that for Figure 1.}
fig_filepath: {Fig1: test/test_fig1.pdf, Fig2: test/test_fig2.pdf}
fig_title: {Fig1: This is the caption for Figure 1., Fig2: The Figure 2 caption.}
header-includes: ['\usepackage{graphicx}', '\usepackage{wrapfig}', '\usepackage[figurename=Fig.,labelfont={it}]{caption}']
macro_idvars: [fig_title, fig_caption, fig_filepath]
macro_proc: {figure: test/templates/latex_figure.template, include: template_include,
  wrapfig: template_figwrap}
template_figwrap: '\begin{wrapfigure}{$side}{$width\textwidth}

  \includegraphics[width=$width\textwidth]{$id(fig_filepath)}

  \caption{\textbf{$id(fig_title)} $id(fig_caption)}

  \label{$id}

  \end{wrapfigure}

  '
template_include: '$file

  '
---

\begin{figure}[!h]
\centering
\includegraphics[width=0.5\textwidth]{test/test_fig1.pdf}\vspace{-10pt}%
\caption{\textbf{This is the caption for Figure 1.} It describes what Figure 1 shows, and perhaps how to interpret it. It may include details of the layout, or note landmarks and other things of interest.}
\label{Fig1}
\end{figure}


Fig. \ref{Fig1} is a good-looking figure, complete with a title, and caption. 
The particular template used isn't much different than what you get with standard pandoc figures, but it does show what is possible with macros. 

\begin{wrapfigure}{L}{0.3\textwidth}
\includegraphics[width=0.3\textwidth]{test/test_fig2.pdf}
\caption{\textbf{The Figure 2 caption.} This caption is different than that for Figure 1.}
\label{Fig2}
\end{wrapfigure}


Fig. \ref{Fig2} implements a wrapfig environment, and like Fig. \ref{Fig1} it also has a title, and caption.
The text of this paragraph should be wrapping around the figure. These demonstration macros are obviously latex, but html, or whatever else you need are just as easy to implement. 
One reason to use macros is it allows you to neatly organize everything in metadata or files as convenient, rather than spread out across the document. 
It also allows you to re-use bits of text like captions, which is very useful when needed. 
But mostly, it lets you implement arbitrary formatting that sidesteps the limitations of pandoc. 

You can also implement a simple file include macro. Here, text from the file src/included_tex.md is inserted:

file://src/included_text.md


Notice that no ID is specified. It isn't needed unless you use idvariables, which use the id to lookup the value to insert.