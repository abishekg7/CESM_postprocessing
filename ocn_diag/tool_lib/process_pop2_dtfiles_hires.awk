#! /usr/bin/awk -f
#
# process_pop2_logfiles.globaldiag.awk -- 
#	Extracts global mean diagnostics information
#	from pop2 log files; outputs monthly and/or
#	annual time series files.
#
# Usage: process_pop2_logfiles.globaldiag.awk <pop2logfile(s)>
#
# Output files are:
#	"diagts_nino.asc"  , ascii table of monthly/annual Nino diagnostics 
#	"diagts_3d.asc"  , ascii table of monthly/annual 3-d (and some 2-d) field diagnostics 
#	"diagts_hflux.asc"  , ascii table of monthly/annual surface heat flux diagnostics 
#	"diagts_fwflux.asc"  , ascii table of monthly/annual surface freshwater flux diagnostics 
#	"diagts_cfc.asc"  , ascii table of monthly/annual CFC11 & CFC12 diagnostics 
#	"diagts_precfactor.asc"  , ascii table of annual precip factor
#	"diagts_info.asc"  , ascii table of log file info
#
BEGIN {
}
{
   deciyear = sprintf("%12.5f",$1)
   deciyear = deciyear/365. 
   mtransport = $2 
   htransport = $3 
   stransport = $4 
   name = $5 
   name2 = $6 
   name3 = $7 
   if (name == "ACC-Drake" || name == "Drake") { 
     if (! (deciyear in recordedthistime)) {
        ++timecnt
        recordedthistime[deciyear] = 1
        modeltime[timecnt] = deciyear
     }
     mtrans_drake[deciyear] = mtransport
     htrans_drake[deciyear] = htransport
     strans_drake[deciyear] = stransport
   }
   if (name == "Mozambique") { 
     mtrans_mozam[deciyear] = mtransport
     htrans_mozam[deciyear] = htransport
     strans_mozam[deciyear] = stransport
   }
   if (name == "Bering") { 
     mtrans_bering[deciyear] = mtransport
     htrans_bering[deciyear] = htransport
     strans_bering[deciyear] = stransport
   }
   if (name == "Northwest") { 
     mtrans_nw[deciyear] = mtransport
     htrans_nw[deciyear] = htransport
     strans_nw[deciyear] = stransport
   }
   if (name == "Indonesian") { 
     mtrans_ITF[deciyear] = mtransport
     htrans_ITF[deciyear] = htransport
     strans_ITF[deciyear] = stransport
   }
   if (name == "Florida") {
     mtrans_florida[deciyear] = mtransport
     htrans_florida[deciyear] = htransport
     strans_florida[deciyear] = stransport
   }
   if (name == "Windward") {
     mtrans_WP[deciyear] = mtransport
     htrans_WP[deciyear] = htransport
     strans_WP[deciyear] = stransport
   }
   if (name == "Gibraltar") {
     mtrans_gib[deciyear] = mtransport
     htrans_gib[deciyear] = htransport
     strans_gib[deciyear] = stransport
   }
   if (name == "Nares") {
     mtrans_nares[deciyear] = mtransport
     htrans_nares[deciyear] = htransport
     strans_nares[deciyear] = stransport
   }
}

END {
     # Drake Passage 
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.drake.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_drake[y], \
	"  ",htrans_drake[y],"  ",strans_drake[y]) >> "transports.drake.asc"
     }
     close("transports.drake.asc")

     # Mozambique Channel
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.mozambique.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_mozam[y], \
        "  ",htrans_mozam[y],"  ",strans_mozam[y]) >> "transports.mozambique.asc"
     }
     close("transports.mozambique.asc")

     # Bering Strait
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.bering.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_bering[y], \
        "  ",htrans_bering[y],"  ",strans_bering[y]) >> "transports.bering.asc"
     }
     close("transports.bering.asc")

     # Northwest Passage
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.nwpassage.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_nw[y], \
        "  ",htrans_nw[y],"  ",strans_nw[y]) >> "transports.nwpassage.asc"
     }
     close("transports.nwpassage.asc")

     # Indonesian Throughflow
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.itf.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_ITF[y], \
        "  ",htrans_ITF[y],"  ",strans_ITF[y]) >> "transports.itf.asc"
     }
     close("transports.itf.asc")

     # Florida Strait
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.florida.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_florida[y], \
        "  ",htrans_florida[y],"  ",strans_florida[y]) >> "transports.florida.asc"
     }
     close("transports.florida.asc")

     # Windward Passage
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.windward.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_WP[y], \
        "  ",htrans_WP[y],"  ",strans_WP[y]) >> "transports.windward.asc"
     }
     close("transports.windward.asc")

     # Gibraltar
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.gibraltar.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_gib[y], \
        "  ",htrans_gib[y],"  ",strans_gib[y]) >> "transports.gibraltar.asc"
     }
     close("transports.gibraltar.asc")
 
     # Nares Strait
     printf("%12s%15s%15s%15s\n","Year","Mass","Heat","Salt") > "transports.nares.asc"
     for (x = 1; x <= timecnt; x++) {
       y = modeltime[x]
       printf("%12.5f%2s%+.6E%2s%+.6E%2s%+.6E\n",y,"  ",mtrans_nares[y], \
        "  ",htrans_nares[y],"  ",strans_nares[y]) >> "transports.nares.asc"
     }
     close("transports.nares.asc")


}
