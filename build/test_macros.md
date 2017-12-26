---
header-includes:
    - \usepackage{graphicx}
    - \usepackage{wrapfig}
    - \usepackage[figurename=Fig.,labelfont={it}]{caption}

# Needed for the latex figure environment, since it is not available in the default document class 
documentclass: article

# idvar : dict
# idvars allow you to replace variables in your template with text based on the id of a given macro. 
# For example, say you have two figures in your manuscript. You want to process each figure macro using 
# a latex figure template. But each figure should have different captions, different file paths, etc. 
# Here, Fig1 and Fig2 are the ids. Use them in the markdown body to identify each macro (![:macro_name ](Fig1)).
# When a macro is found with a Fig1 id and the template contains the var $id(fig_caption), it will be replaced
# with "This is the caption for Figure 1."
# 
# Each idvar metadata variable should be a dict, with keys as ids and vals as the text to replace. The name of 
# the variable should be the name of an idvar in the template (ie $id(var_name)). Eeach idvar should be listed
# in macro_idvars.
# 
fig_title:
    Fig1: This is the caption for Figure 1. 
    Fig2: The Figure 2 caption.

fig_caption:
    Fig1: It describes what Figure 1 shows, and perhaps how to interpret it. It may include details of the layout, or note landmarks and other things of interest. 
    Fig2: This caption is different than that for Figure 1. 

fig_filepath:
    Fig1: test/test_fig1.pdf 
    Fig2: test/test_fig2.pdf 

# macro_idvars : list
# List of metadata variable names to use to look for idvars. 
macro_idvars:
    - fig_title
    - fig_caption
    - fig_filepath

# macro_proc : dict
# Keys specify the macro name to search for (ie.: ![:macro_name var1=some value]). Vals specify the template to use. 
# Templates can be file paths, or other metadata variables.
macro_proc:
    figure: test/templates/latex_figure.template
    wrapfig: template_figwrap
    include: template_include

# template : str
# 
# template_figure example is for simple latex figures. 
# The macro id (param in parentheses: eg., Fig1) is the label. Then in your body text, you 
# can reference the figure with tex: \ref{Fig1}.
# Other parameters are:
#   $width : The figure width, as proportion of available space
#   $id(title) : The first line of caption, will be bold
#   $id(fig_caption) : The figure caption
#   $id(fig_filepath) : The path to the figure, absolute or relative 
# 
# As implemented, this macro/template doesn't do much more than pandoc's standard figure 
# method, except a bit more parametric control, and the ability to store variables in metadata
# rather than in the macro itself, which can be unruly for, eg., long figure captions. But it  
# does demonstrate how more complex macros can be easily implemented.
#template_figure: |
#    \begin{figure}[!h]
#    \centering
#    \includegraphics[width=$width\textwidth]{$id(fig_filepath)}\vspace{-10pt}%
#    \caption{\textbf{$id(fig_title)} $id(fig_caption)}
#    \label{$id}
#    \end{figure}

# template_figwrap example implements a wrapfigure latex environment. 
# The macro id (param in parentheses) is the label. Other parameters are:
#   $side : The side of the page to position the figure, L or R
#   $width : The figure width, as proportion of available space
#   $id(title) : The first line of caption, will be bold
#   $id(fig_caption) : The figure caption
#   $id(fig_filepath) : The path to the figure, absolute or relative 
# 
# Requires \usepackage{wrapfig} in headers-include
template_figwrap: |
    \begin{wrapfigure}{$side}{$width\textwidth}
    \includegraphics[width=$width\textwidth]{$id(fig_filepath)}
    \caption{\textbf{$id(fig_title)} $id(fig_caption)}
    \label{$id}
    \end{wrapfigure}

# template_include example can be useful with a generic include macro
# Macro usage: ![:include file=file://path/to/file]()
# The use of 'file://' indicates that the string is a file path, rather 
# than a simple string. For absolute paths (on linux), use three slashes:
# file=file:///home/user/path/to/file
template_include: |
    $file
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