#gene expression data
exp <- read.delim("eQTL_gene_exp.tpms.tsv", 
                  header = TRUE, 
                  sep = "\t", 
                  comment.char = "#", 
                  stringsAsFactors = FALSE, 
                  check.names = FALSE)

exp <- na.omit(exp)

# gene names as columns
exp <- t(exp)
exp_data <- as.matrix(exp)
mode(exp_data) <- "numeric" # should be numeric

#transcription factor 
tf_ID <- read.csv("tf_list.txt")

#TIGRESS only accepts gene names that match the tf_list and gene expression data
matched_tf_list <- tf_list[tf_list %in% colnames(exp)]

#####################
#changing source code (LARS to use.Gram = FLASE, to avoid the loop as n, number of samples is < m, number of predictors/genes/columns)
#tigress:::stabilityselection
stabilityselection_mod <- function (x, y, nsplit = 100, nstepsLARS = 20, alpha = 0.2, scoring = "area") 
{
    if (!is.numeric(y) || sd(y) == 0) 
        stop("y should be a vector of scalars not constant.")
    n <- nrow(x)
    p <- ncol(x)
    halfsize <- as.integer(n/2)
    freq <- matrix(0, nstepsLARS, p)
    i <- 0
    while (i < 2 * nsplit) {
        xs <- t(t(x) * runif(p, alpha, 1))
        badsplit <- TRUE
        while (badsplit) {
            perm <- sample(n)
            i1 <- perm[1:halfsize]
            i2 <- perm[(halfsize + 1):n]
            if (max(sd(y[i1]), sd(y[i2])) > 0) {
                badsplit = FALSE
            }
        }
        if (sd(y[i1] > 0)) {
            r <- lars(xs[i1, ], y[i1], max.steps = nstepsLARS, 
                normalize = FALSE, trace = FALSE)
            freq <- freq + abs(sign(r$beta[2:(nstepsLARS + 1), 
                ]))
            i <- i + 1
        }
        if (sd(y[i2] > 0)) {
            r <- lars(xs[i2, ], y[i2], max.steps = nstepsLARS, 
                normalize = FALSE, trace = FALSE, use.Gram =  FALSE)
            freq <- freq + abs(sign(r$beta[2:(nstepsLARS + 1), 
                ]))
            i <- i + 1
        }
    }
    freq <- freq/i
    if (scoring == "area") 
        score <- apply(freq, 2, cumsum)/seq(nstepsLARS)
    else score <- apply(freq, 2, cummax)
    invisible(score)
}

#stabselonegene
stabselonegene <- function(itarget) {
  if (verb) cat(".")
  
  targetname <- targetlist[itarget]
  predTF <- tflist != targetname
  
  r <- stabilityselection_mod(
    as.matrix(expdata[, tfindices[predTF]]),
    as.matrix(expdata[, targetname]),
    nsplit = nsplit,
    nstepsLARS = nstepsLARS,
    alpha = alpha
  )
  
  sc <- array(0, dim = c(ntf, scorestokeep), dimnames = list(tflist, seq(scorestokeep)))
  
  if (allsteps) {
    sc[predTF, ] <- t(r)
  } else {
    sc[predTF, ] <- t(r[nstepsLARS, ])
  }
  
  invisible(sc)
}
 
#stabilityselection_mod()
stabilityselection_mod <- function(x, y, nsplit = 100, nstepsLARS = 20, alpha = 0.2, scoring = "area") {
  if (!is.numeric(y) || sd(y) == 0) 
    stop("y should be a vector of scalars not constant.")
  
  n <- nrow(x)
  p <- ncol(x)
  halfsize <- as.integer(n / 2)
  freq <- matrix(0, nstepsLARS, p)
  i <- 0
  
  while (i < 2 * nsplit) {
    xs <- t(t(x) * runif(p, alpha, 1))
    badsplit <- TRUE
    
    while (badsplit) {
      perm <- sample(n)
      i1 <- perm[1:halfsize]
      i2 <- perm[(halfsize + 1):n]
      if (max(sd(y[i1]), sd(y[i2])) > 0) {
        badsplit = FALSE
      }
    }
    
    if (sd(y[i1]) > 0) {
      r <- lars(xs[i1, ], y[i1], max.steps = nstepsLARS, normalize = FALSE, trace = FALSE, use.Gram = FALSE)
      freq <- freq + abs(sign(r$beta[2:(nstepsLARS + 1), ]))
      i <- i + 1
    }
    
    if (sd(y[i2]) > 0) {
      r <- lars(xs[i2, ], y[i2], max.steps = nstepsLARS, normalize = FALSE, trace = FALSE, use.Gram = FALSE)
      freq <- freq + abs(sign(r$beta[2:(nstepsLARS + 1), ]))
      i <- i + 1
    }
  }
  
  freq <- freq / i
  
  if (scoring == "area") {
    score <- apply(freq, 2, cumsum) / seq(nstepsLARS)
  } else {
    score <- apply(freq, 2, cummax)
  }
  
  invisible(score)
}

#define tigress_mod()
tigress_mod <- function(expdata, tflist = colnames(expdata), targetlist = colnames(expdata), 
                        alpha = 0.2, nstepsLARS = 5, nsplit = 100, normalizeexp = TRUE, 
                        scoring = "area", allsteps = TRUE, verb = FALSE, usemulticore = FALSE) {
  
  if (usemulticore) {
    require(parallel)
  }
  
  genenames <- colnames(expdata)
  ngenes <- length(genenames)
  
  if (normalizeexp) 
    expdata <- scale(expdata)
  
  if (nstepsLARS > length(tflist) - 1) {
    nstepsLARS <- length(tflist) - 1
    if (nstepsLARS == 0) {
      cat("Too few transcription factors! \n", stderr())
    }
    if (verb) {
      cat(paste("Variable nstepsLARS was changed to: ", nstepsLARS, "\n"))
    }
  }
  
  ntf <- length(tflist)
  tfindices <- match(tflist, genenames)
  
  if (max(is.na(tfindices))) stop("Error: could not find all TF in the gene list!")
  
  ntargets <- length(targetlist)
  targetindices <- match(targetlist, genenames)
  
  if (max(is.na(targetindices))) stop("Error: could not find all targets in the gene list!")
  
  scorestokeep <- if (allsteps) nstepsLARS else 1
  
  score <- list()
  
  stabselonegene <- function(itarget) {
    if (verb) cat(".")
    
    targetname <- targetlist[itarget]
    predTF <- !match(tflist, targetname, nomatch = 0)
    
    r <- stabilityselection_mod(
      as.matrix(expdata[, tfindices[predTF]]),
      as.matrix(expdata[, targetname]),
      nsplit = nsplit,
      nstepsLARS = nstepsLARS,
      alpha = alpha
    )
    
    sc <- array(0, dim = c(ntf, scorestokeep), dimnames = list(tflist, seq(scorestokeep)))
    
    if (allsteps) {
      sc[predTF, ] <- t(r)
    } else {
      sc[predTF, ] <- t(r[nstepsLARS, ])
    }
    
    invisible(sc)
  }
  
  if (usemulticore) {
    if (requireNamespace("foreach") && foreach::getDoParRegistered()) {
      `%dopar%` = foreach::`%dopar%`
      score <- foreach::foreach(i = seq(ntargets), .packages = c("lars")) %dopar% stabselonegene(i)
    } else {
      score <- mclapply(seq(ntargets), stabselonegene, mc.cores = detectCores() - 1)
    }
  } else {
    score <- lapply(seq(ntargets), stabselonegene)
  }
  
  edgepred <- list()
  for (i in seq(scorestokeep)) {
    edgepred[[i]] <- matrix(unlist(lapply(score, function(x) x[, i, drop = FALSE])), nrow = ntf)
    rownames(edgepred[[i]]) <- tflist
    colnames(edgepred[[i]]) <- targetlist
  }
  
  if (allsteps) {
    return(edgepred)
  } else {
    return(edgepred[[1]])
  }
}
#####################     
result <- tigress_mod(
  exp,
  tflist = matched_tf_list,
  targetlist = colnames(exp_data), 
  alpha = 0.2, #less randomization → more stable
  nstepsLARS = 5, #Controls how many TFs are gradually added to explain the target gene’s expression
  nsplit = 100, # random data subsets used to test the robustness of inferred TF–target links.
  normalizeexp = TRUE, #Ensures all genes have comparable scales (mean 0, variance 1)
  scoring = "area", #Uses the area under the stability curve
  allsteps = TRUE, #considers all selected TFs up to nstepsLARS in the final score.
  verb = FALSE, #Controls verbosity (printing progress messages).
  usemulticore = FALSE #Runs on a single core #Recommend: TRUE for large dataset.
)
