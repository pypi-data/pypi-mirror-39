import sys, os, math, re, numpy as np

def readSpeciesFilter(fname) :
    f = {}
    if os.path.isfile(fname) :
        with open(fname) as fin :
            for line in fin :
                part = line.rstrip().split('\t')
                if len(part) == 1 or part[1] == '' :
                    f[part[0]] = '*'
                else :
                    f[part[0]] = part[1]
    else :
        f[fname] = '*'
    return f
def report(fnames, args) :
    pathogens = {
        'Gardnerella ': '* vaginosis',
        ' saprophyticus': '*** urinary tract infections',
        ' bovis': '** bovine pathogen',
        ' parasuis': '* swine pathogen',
        ' suis' : '** swine pathogen',
        'Leptospira ':'** Leptospirosis',
        'Corynebacterium ulcerans':'***',
        'Mycobacterium ulcerans':'***',
        'Chlamydia ': '***',
        'enteric': '**',
        'Listeria monocytogenes':'* listeriosis',
        'Ureaplasma ':'*** urogenital diseases',
        'Ehrlichia ': '*** Ehrlichiosis',
        'Helicobacter ': '** Peptic ulcer',
        'Nocardia asteroides': '** Nocardiosis',
        'Francisella ': '*** Tularemia',
        'Chlamydophila ': '*** Psittacosis',
        'Mycobacterium avium' : '** animal pathogen',
        'tuberculosis':'*** TB',
        ' pestis':'**** plague',
        'Rickett': '*** Rickettsia',
        'Brucella ': '*** Brucellosis',
        ' pylori': '**** Peptic ulcer',
        'pertussis': '**** Whooping cough',
        'Bartonella ': '***',
        ' diphtheriae': '*** Diphtheria',
        'Shigella ': '**** Shigellosis',
        ' cholerae': '**** Cholera',
        'mallei': '** animal pathogen',
        ' leprae': '*** Leprosy ',
        ' africanum': '*** TB',
        ' gonorrhoeae': '** Gonorrhea',
        ' trachomatis': '*** Trachoma',
        ' canettii': '** TB',
        'pallidum': '**** syphilis',
        'Borrelia ': '**** Lyme disease/Relapsing fever',
        'Leishmania ': '**** Parasite',
        'Apicomplexa': '*** Parasite',
        ' pneumoniae': '** pneumonia',
        'Legionella pneumophila':'* legionellosis',
        'Salmonella ':'**** Salmonellosis/Typhoid',
        'Bacillus anthracis':'** Anthrax',
        'Campylobacter jejuni':'*** campylobacteriosis',
        ' enterocolitica':'** enterocolitis',
        'Campylobacter coli':'*** campylobacteriosis',
        'Staphylococcus aureus':'*',
        'Staphylococcus epidermidis':'*',
        'Pseudomonas aeruginosa':'*',
        'Moraxella catarrhalis':'** chronic chest disease',
        'Moraxella lacunata':'* blepharoconjunctivitis',
        ' pyogenes':'*',
        'Escherichia ':'*',
        'Trichomonas vaginalis':'*** trichomoniasis',
        'Adenoviridae':'**** Virus',
        'Picornaviridae':'**** Virus',
        'Herpesviridae':'**** Virus',
        'Hepadnaviridae':'**** Virus',
        'Flaviviridae':'**** Virus',
        'Retroviridae':'**** Virus',
        'Orthomyxoviridae':'**** Virus',
        'Paramyxoviridae':'**** Virus',
        'Papovaviridae':'**** Virus',
        'Polyomavirus':'**** Virus',
        'Rhabdoviridae':'**** Virus',
        'Togaviridae':'**** Virus',
        'Filoviridae':'**** Virus',
        'Poxviridae':'**** Virus',
        'Neisseria meningitidis':'** meningitis',
        'Burkholderia cenocepacia':'** cepacia syndrome',
        
        'Porphyromonas gingivalis':'** red_complex',
        'Tannerella forsythia':'** red_complex',
        'Treponema denticola':'** red_complex',
        
        'Fusobacterium nucleatum':'* Orange_complex',
        'Campylobacter rectus': '* Orange_complex',
        'Campylobacter showae': '* Orange_complex', 
        'Campylobacter gracilis' : '* Orange_complex',
        'Eubacterium ': '* Orange_complex',
        'treptococcus micros':'* Orange_complex',
        'Prevotella intermedia' : '* Orange_complex', 
        'Prevotella nigrescens' : '* Orange_complex', 
        'Streptococcus constellatus' : '* Orange_complex', 
        
        
        'Actinomyces naeslundii':'* Blue_complex', 
        'Actinomyces viscosus':'* Blue_complex', 
        'Veillonella parvula':'* Purple_complex',
        'Actinomyces odontolyticus' : '* Purple_complex', 
        
        'Aggregatibacter actinomycetemcomitans':'* HACEK/Green_complex',
        'Eikenella corrodens':'* HACEK/Green_complex',
        'Capnocytophaga ':'* Green_complex',

        'Entamoeba gingivalis':'* periodontitis',
        'Trichomonas tenax':'* periodontitis',
        'Fusobacterium polymorphum':'* periodontitis',
        'Fusobacterium necrophorum':'** Lemierre syndrome',
        'Streptobacillus moniliformis':'** Haverhill fever', 
        'Haemophilus influenzae':'* HACEK',
        'Haemophilus parainfluenzae':'* HACEK',
        'Haemophilus haemolyticus':'* HACEK',
        'Haemophilus parahaemolyticus':'* HACEK',
        'Aggregatibacter segnis':'* HACEK',
        'Aggregatibacter aphrophilus':'* HACEK',
        'Aggregatibacter paraphrophilus':'* HACEK',
        'Cardiobacterium hominis':'* HACEK',
        'Cardiobacterium valvarum':'* HACEK',
        'Kingella kingae':'* HACEK',
        'Kingella denitrificans':'* HACEK',
        'Tropheryma whipplei':'* Whipple disease',
        'Arcanobacterium haemolyticum':'* Arcanobacterium haemolyticum infection',
        'Erysipelothrix rhusiopathiae':'* erysipeloid',
        'Streptococcus mutans': '** dental_caries',
        'Streptococcus sobrinus': '** dental_caries',
    }
    if  args['speciesFilter'] :
        pathogens = readSpeciesFilter(args['speciesFilter'])

    taxa = {'Unknown':['Dark Matter', 0.]}
    levels = args.get('tag', 's').split(',')
    data = {}
    fnames = [fname for fname in [ fname if os.path.isfile(fname) else os.path.join(fname, 'profile.txt') for fname in fnames ] if os.path.isfile(fname)]
    if args.get('path', None) :
        for path, subdirs, files in os.walk(args['path']) :
            for fname in files :
                if fname == 'profile.txt' :
                    fnames.append(os.path.join(path, fname))
    for fname in fnames :
        data[fname] = {}
        with open(fname) as fin :
            header = fin.readline().strip().split('\t')
            n_tot, n_found = int(header[1]), float(header[2])
            dark_matter = n_tot if args.get('absolute', False) else 100.
            for line in fin :
                for level_id, level in enumerate(levels) :
                    if line.startswith(level) :
                        group, p1, p2, taxon = line.strip().split('\t')
                        p2 = float(p2)
                        taxon = taxon.rsplit(' (', 1)[0]
                        if (p2*n_found)/n_tot < args.get('low', 0.) : 
                            continue
                        if args.get('absolute', False) :
                            n_read = int(round(float(p2)/100. * n_found, 0))
                            if n_read > 0 :
                                if level_id == 0 :
                                    dark_matter -= n_read
                                data[fname][group] = n_read
                                if group not in taxa :
                                    taxa[group] = [taxon, 0.]
                                taxa[group][1] += n_read
                        else :
                            p_read = (p2*n_found)/n_tot
                            if level_id == 0 :
                                dark_matter -= p_read
                            data[fname][group] = p_read
                            if group not in taxa :
                                taxa[group] = [taxon, 0.]
                            taxa[group][1] += p_read
            data[fname]['Unknown'] = dark_matter
    pathogens = sorted(pathogens.items(), key=lambda x:x[1])
    taxa_list = [t[0] for t in sorted(taxa.items(), key=lambda x:x[1][1], reverse=True)]
    mat = [['#Group', '#Label'] + [ fn.rsplit('/', 1)[0] for fn in fnames ] + ['#Species', '#Taxon']]
    #print '#Group\t#Label\t{0}\t#Species\t#Taxon'.format('\t'.join([ fn.rsplit('/', 1)[0] for fn in fnames]))
    for group in taxa_list :
        label = 'non'
        taxon = taxa[group][0].rsplit('(', 1)[0]
        for p, t in pathogens :
            if re.findall(p, taxon) :
                label = t
                break
        if label == 'non' and (args['speciesFilter'] or args['sampleFilter']) :
            continue
        try:
            species = taxa[group][0].split('|')[7] if taxa[group][0] != 'Dark Matter' else '-'
        except :
            species = '-'
        mat.append([group, label ] + [ str(data[fn].get(group, 0)) for fn in fnames ] + [species, taxa[group][0]])
        #print '{0}\t{3}\t{1}\t{4}\t{2}'.format(group, '\t'.join([ str(data[fn].get(group, 0)) for fn in fnames ]), taxa[group][0], label, species)
    mat = np.array(mat, dtype=str)
    if args['sampleFilter'] and mat.shape[0] > 1 :
        d = mat[1:, 2:-2].astype(float)
        dd = np.concatenate([[0, 1] , np.where(np.sum(d, 0)>0)[0]+2, [-2, -1]])
        mat = mat[:,dd]

    if args['inverse'] :
        mat = mat.T
        
    for m in mat :
        print '\t'.join(m)

if __name__ == '__main__' :
    report(sys.argv[1:], {})
