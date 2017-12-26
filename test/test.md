---
header-includes:
    - \usepackage{graphicx}
    - \usepackage{wrapfig}
    - \usepackage[figurename=Fig.,labelfont={it}]{caption}

# idvar : dict
# idvars allow you to replace variables in your template with text based on the id of a given macro. 
# For example, say you have two figures in your manuscript. You want to process each figure macro using 
# a latex figure template. But each figure should have different captions, different file paths, etc. 
# Here, Fig1 and Fig2 are the ids. Use them in the markdown body to identify each macro (![:macro_name ](Fig1)).
# When a macro is found with a Fig1 id and the template contains the var $id(fig_caption), it will be replaced
# with "This is the caption for Figure 1."
# 
# Each idvar metadata variable should be a dict, with keys as ids and vals as the text to replace. The name of 
# the variable should be the name of an idvar in the template (ie $id(var_name))
# 
fig_caption:
    Fig1: This is the caption for Figure 1. 
    Fig2: The Figure 2 caption is different. 

fig_file:
    Fig1: src/test_fig1.pdf 
    Fig2: src/test_fig2.pdf 

# macro_idvars : list
# List of metadata variable names to use for idvars. 
macro_idvars:
    - fig_caption
    - fig_file

# macro_proc : dict
# Keys specify the macro name to search for (ie.: ![:macro_name width=0.4]). Vals specify the template to use. 
# Templates can be file paths, or other metadata variables.
macro_proc:
    figure_macro: macro_template

macro_template: |
    \begin{figure}[!h]
    \label{$id}
    \includegraphics[width=$width\textwidth]{$id(fig_file)}\vspace{-10pt}%
    \caption{{\bf $id(title)} $id(fig_caption)}
    \end{figure}

---
Here is some {++added ++}text. There is also an addition {++that now contains a fair amount of text++}. This is a{-- wanted--} deletion. {>>@CAB Here is a comment all by itself<<}And here is a really {~~good~>bad~~}{>>@CAB better<<} substitution, which is illustrated in Fig. \ref{Fig1}. All of this is actually true [@ieee_ieee_1969].

![:figure_macro width=0.4](Fig1)

![:figure_macro width=0.4](Fig2)
