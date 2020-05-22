select liq."data_da_liquidação", emp."data_emissão_empenho", emp."data_de_homologação", pag."data_do_pagamento"
from credores_liquidacoes liq
inner join detalhes_emp emp on liq."empenho" = emp."número_do_empenho"
inner join detalhes_emp emp on lower(liq."credor") = lower(emp."credor")
inner join credores_pagamentos pag on lower(liq."credor") = lower(pag."credor")
inner join credores_pagamentos pag on liq."empenho" = pag."empenho"
inner join credores_pagamentos pag on liq."número_de_liquidação" = pag."número_de_liquidação"


/* tempo entre homologacao e empenho */
emp."data_emissão_empenho" - emp."data_de_homologação"

/* tempo entre empenho e liquidacao */
liq."data_da_liquidação" - emp."data_emissão_empenho"

/* tempo entre liquidacao e pagamento*/
pag."data_do_pagamento" - liq."data_da_liquidação"

/* tempo total */
pag."data_do_pagamento" - liq."data_da_liquidação" - emp."data_emissão_empenho" - emp."data_de_homologação"