"""
Script de Seed (Carga Inicial) para o Supabase.
Popula o catálogo de obras (com pôsteres reais do TMDB) e contas de teste dos alunos.
Pode ser executado a qualquer momento com:
    python seed.py
"""

import sys
from database import supabase
from security import hash_password

USERS_SEED = [
    {
        "name": "Aluno Teste (Geral)",
        "email": "teste@app.com",
        "password": "123456"
    },
    {
        "name": "Professor Responsável",
        "email": "professor@ifms.edu.br",
        "password": "123456"
    },
    {
        "name": "Lucas Aluno",
        "email": "lucas@estudante.ifms.edu.br",
        "password": "123456"
    },
    {
        "name": "Mariana Estudante",
        "email": "mariana@estudante.ifms.edu.br",
        "password": "123456"
    },
    {
        "name": "Gabriel Mobile",
        "email": "gabriel@estudante.ifms.edu.br",
        "password": "123456"
    }
]

ITEMS_SEED = [
    # AÇÃO
    {
        "title": "Matrix",
        "synopsis": "Um programador de computador descobre que a realidade que vive é uma simulação criada por máquinas e se junta a uma rebelião para libertar a humanidade.",
        "category": "Ação",
        "release_year": 1999,
        "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
    },
    {
        "title": "Batman: O Cavaleiro das Trevas",
        "synopsis": "Com a ajuda do tenente Jim Gordon e do promotor Harvey Dent, Batman combate o crime organizado de Gotham, mas é desafiado pela mente anárquica do Coringa.",
        "category": "Ação",
        "release_year": 2008,
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
    },
    {
        "title": "Mad Max: Estrada da Fúria",
        "synopsis": "Em um mundo pós-apocalíptico desértico, Max se une à Imperatriz Furiosa em uma fuga frenética contra o tirano Immortan Joe.",
        "category": "Ação",
        "release_year": 2015,
        "poster_url": "https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg"
    },
    {
        "title": "Vingadores: Ultimato",
        "synopsis": "Após os eventos devastadores de Guerra Infinita, o universo está em ruínas. Os Vingadores restantes se reúnem para desfazer as ações de Thanos.",
        "category": "Ação",
        "release_year": 2019,
        "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
    },
    {
        "title": "John Wick: De Volta ao Jogo",
        "synopsis": "Um assassino aposentado volta à ativa em busca de vingança contra os criminosos que tiraram tudo o que ele mais amava.",
        "category": "Ação",
        "release_year": 2014,
        "poster_url": "https://image.tmdb.org/t/p/w500/fZPSMVwqnnq7ioxsPV9uzirzvyY.jpg"
    },
    {
        "title": "Top Gun: Maverick",
        "synopsis": "Após mais de trinta anos de serviço como um dos melhores aviadores da Marinha, Pete Mitchell treina um destacamento de graduados para uma missão especializada.",
        "category": "Ação",
        "release_year": 2022,
        "poster_url": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg"
    },

    # FICÇÃO CIENTÍFICA
    {
        "title": "Interestelar",
        "synopsis": "Com o futuro da Terra em perigo, um grupo de astronautas viaja através de um buraco de minhoca em busca de um novo lar para a humanidade.",
        "category": "Ficção Científica",
        "release_year": 2014,
        "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
    },
    {
        "title": "A Origem (Inception)",
        "synopsis": "Um ladrão habilidoso que rouba segredos do inconsciente durante o estado de sono recebe uma tarefa inversa: implantar uma ideia na mente de um herdeiro.",
        "category": "Ficção Científica",
        "release_year": 2010,
        "poster_url": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg"
    },
    {
        "title": "Blade Runner 2049",
        "synopsis": "Trinta anos após os acontecimentos do primeiro filme, um novo Blade Runner descobre um segredo enterrado há muito tempo que tem o potencial de mergulhar a sociedade no caos.",
        "category": "Ficção Científica",
        "release_year": 2017,
        "poster_url": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"
    },
    {
        "title": "Duna",
        "synopsis": "Paul Atreides, um jovem brilhante e talentoso, deve viajar para o planeta mais perigoso do universo para garantir o futuro de sua família e seu povo.",
        "category": "Ficção Científica",
        "release_year": 2021,
        "poster_url": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg"
    },
    {
        "title": "De Volta para o Futuro",
        "synopsis": "Marty McFly viaja acidentalmente trinta anos para o passado no DeLorean do Dr. Emmett Brown e deve garantir que seus pais se apaixonem.",
        "category": "Ficção Científica",
        "release_year": 1985,
        "poster_url": "https://image.tmdb.org/t/p/w500/iA5pZp3BcxT33vG293cI62fC9rL.jpg"
    },
    {
        "title": "Ex Machina",
        "synopsis": "Um jovem programador é selecionado para participar de um experimento inovador em inteligência sintética avaliando os traços humanos de uma humanoide IA.",
        "category": "Ficção Científica",
        "release_year": 2014,
        "poster_url": "https://image.tmdb.org/t/p/w500/btbUS5qc1t5GFv3m0AezZpX8u4I.jpg"
    },

    # ANIMAÇÃO
    {
        "title": "Homem-Aranha no Aranhaverso",
        "synopsis": "Miles Morales se torna o novo Homem-Aranha e une forças com outras versões do herói de dimensões paralelas para salvar o multiverso.",
        "category": "Animação",
        "release_year": 2018,
        "poster_url": "https://image.tmdb.org/t/p/w500/8j58iEBw9pOXFD2L0nt0ZXeHviB.jpg"
    },
    {
        "title": "A Viagem de Chihiro",
        "synopsis": "Durante a mudança de sua família para o subúrbio, uma garota de 10 anos vagueia por um mundo governado por deuses, bruxas e espíritos.",
        "category": "Animação",
        "release_year": 2001,
        "poster_url": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"
    },
    {
        "title": "Toy Story",
        "synopsis": "Um boneco vaqueiro se sente ameaçado e com ciúmes quando um novo astronauta se torna o brinquedo favorito no quarto de um garoto.",
        "category": "Animação",
        "release_year": 1995,
        "poster_url": "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrFuVJjhab.jpg"
    },
    {
        "title": "Viva: A Vida é uma Festa (Coco)",
        "synopsis": "O aspirante a músico Miguel entra na Terra dos Mortos para encontrar seu tataravô, um cantor lendário, e desvendar um mistério familiar.",
        "category": "Animação",
        "release_year": 2017,
        "poster_url": "https://image.tmdb.org/t/p/w500/g4JgN1eG83pWd9Y4YnQ6gA7x3lq.jpg"
    },
    {
        "title": "Divertida Mente",
        "synopsis": "Após a jovem Riley se mudar para uma nova cidade, suas emoções — Alegria, Tristeza, Medo, Raiva e Nojinho — entram em conflito sobre como navegar sua nova vida.",
        "category": "Animação",
        "release_year": 2015,
        "poster_url": "https://image.tmdb.org/t/p/w500/9z25McugIPxmA589gTGVa48l9qq.jpg"
    },
    {
        "title": "O Rei Leão",
        "synopsis": "O príncipe leão Simba foge de seu reino após a morte de seu pai e aprende o verdadeiro significado de responsabilidade e coragem.",
        "category": "Animação",
        "release_year": 1994,
        "poster_url": "https://image.tmdb.org/t/p/w500/b1Baev79V3y41kZg2Nn0vjB9aQ8.jpg"
    },

    # DRAMA
    {
        "title": "O Poderoso Chefão",
        "synopsis": "O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filho mais relutante.",
        "category": "Drama",
        "release_year": 1972,
        "poster_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
    },
    {
        "title": "Um Sonho de Liberdade",
        "synopsis": "Dois homens presos ao longo de vários anos encontram consolo e redenção através de atos de decência comum.",
        "category": "Drama",
        "release_year": 1994,
        "poster_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
    },
    {
        "title": "Clube da Luta",
        "synopsis": "Um trabalhador de escritório insone e um fabricante de sabão desinibido formam um clube de luta clandestino que evolui para algo muito maior.",
        "category": "Drama",
        "release_year": 1999,
        "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"
    },
    {
        "title": "Forrest Gump",
        "synopsis": "As presidências de Kennedy e Johnson, os eventos do Vietnã e de Watergate se desenrolam da perspectiva de um homem do Alabama com bom coração.",
        "category": "Drama",
        "release_year": 1994,
        "poster_url": "https://image.tmdb.org/t/p/w500/arw2VCBveWOVZr6pxd9XTd1TdQa.jpg"
    },
    {
        "title": "Parasita",
        "synopsis": "A ganância e a discriminação de classe ameaçam a relação simbiótica recém-formada entre a rica família Park e o clã Kim em dificuldades.",
        "category": "Drama",
        "release_year": 2019,
        "poster_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
    },
    {
        "title": "Oppenheimer",
        "synopsis": "A história do cientista americano J. Robert Oppenheimer e seu papel fundamental no desenvolvimento da bomba atômica no Projeto Manhattan.",
        "category": "Drama",
        "release_year": 2023,
        "poster_url": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
    },

    # AVENTURA
    {
        "title": "O Senhor dos Anéis: A Sociedade do Anel",
        "synopsis": "Um manso hobbit do Condado e oito companheiros partem em uma jornada para destruir o poderoso Um Anel e salvar a Terra-média do Lorde das Trevas Sauron.",
        "category": "Aventura",
        "release_year": 2001,
        "poster_url": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cDK6.jpg"
    },
    {
        "title": "Jurassic Park: O Parque dos Dinossauros",
        "synopsis": "Um parque temático pragmático com dinossauros clonados sofre um colapso em seus sistemas de segurança, deixando os visitantes lutando pela sobrevivência.",
        "category": "Aventura",
        "release_year": 1993,
        "poster_url": "https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4ho1.jpg"
    },
    {
        "title": "Harry Potter e o Prisioneiro de Azkaban",
        "synopsis": "Harry Potter, Ron e Hermione retornam a Hogwarts para o terceiro ano escolar, onde investigam o mistério em torno de Sirius Black.",
        "category": "Aventura",
        "release_year": 2004,
        "poster_url": "https://image.tmdb.org/t/p/w500/aWxwnYoe8p2d2fcxOqtvAtJ72Rw.jpg"
    },
    {
        "title": "Piratas do Caribe: A Maldição do Pérola Negra",
        "synopsis": "O ferreiro Will Turner se une ao excêntrico pirata Capitão Jack Sparrow para salvar seu amor da tripulação amaldiçoada e morta-viva de Jack.",
        "category": "Aventura",
        "release_year": 2003,
        "poster_url": "https://image.tmdb.org/t/p/w500/z8onk7LV9M9z9z0m8kL6Lz3yF3A.jpg"
    },
    {
        "title": "Indiana Jones e os Caçadores da Arca Perdida",
        "synopsis": "Em 1936, o arqueólogo e aventureiro Indiana Jones é contratado pelo governo dos EUA para encontrar a lendária Arca da Aliança antes dos nazistas.",
        "category": "Aventura",
        "release_year": 1981,
        "poster_url": "https://image.tmdb.org/t/p/w500/ceG9VzoRAVGwivFU407W8tkNWFi.jpg"
    },

    # TERROR & SUSPENSE
    {
        "title": "O Iluminado",
        "synopsis": "Uma família vai para um hotel isolado durante o inverno, onde uma presença sinistra influencia o pai à violência enquanto seu filho tem clarividências.",
        "category": "Terror",
        "release_year": 1980,
        "poster_url": "https://image.tmdb.org/t/p/w500/b33nnKl1vvg69FagRPTyAhGox4k.jpg"
    },
    {
        "title": "Corra! (Get Out)",
        "synopsis": "Um jovem negro visita os pais brancos de sua namorada em uma propriedade remota, onde descobre um plano sinistro.",
        "category": "Terror",
        "release_year": 2017,
        "poster_url": "https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"
    },
    {
        "title": "Hereditário",
        "synopsis": "Após a morte da matriarca idosa, uma família em luto é assombrada por segredos trágicos e perturbadores sobre sua ancestralidade.",
        "category": "Terror",
        "release_year": 2018,
        "poster_url": "https://image.tmdb.org/t/p/w500/lHV8HHlhwv9R5UMb49MTiO5G4bs.jpg"
    },
    {
        "title": "Um Lugar Silencioso",
        "synopsis": "Em um mundo pós-apocalíptico, uma família é forçada a viver em silêncio absoluto para se esconder de monstros com audição ultrassensível.",
        "category": "Terror",
        "release_year": 2018,
        "poster_url": "https://image.tmdb.org/t/p/w500/nAU74GmpUk7t5iklEp3bufwDq4n.jpg"
    },
    {
        "title": "Seven: Os Sete Crimes Capitais",
        "synopsis": "Dois detetives, um novato e um veterano, caçam um serial killer engenhoso que justifica seus assassinatos hediondos pelos sete pecados capitais.",
        "category": "Suspense",
        "release_year": 1995,
        "poster_url": "https://image.tmdb.org/t/p/w500/69Sns8WoET6C6qYehqpdATdl450.jpg"
    },

    # COMÉDIA
    {
        "title": "O Grande Hotel Budapeste",
        "synopsis": "As aventuras de Gustave H, um lendário concierge em um famoso hotel europeu entre as guerras, e Zero Moustafa, o mensageiro que se torna seu amigo mais confiável.",
        "category": "Comédia",
        "release_year": 2014,
        "poster_url": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWX9ne3rNfg.jpg"
    },
    {
        "title": "O Show de Truman",
        "synopsis": "Um vendedor de seguros descobre que toda a sua vida é, na verdade, um programa de televisão transmitido 24 horas por dia para o mundo inteiro.",
        "category": "Comédia",
        "release_year": 1998,
        "poster_url": "https://image.tmdb.org/t/p/w500/vuza0WqY239ISGhDo8ztmXfBPg2.jpg"
    },
    {
        "title": "O Auto da Compadecida",
        "synopsis": "As aventuras dos nordestinos João Grilo e Chicó, que vivem enganando o povo de uma pequena vila no sertão da Paraíba até prestarem contas com o Todo-Poderoso.",
        "category": "Comédia",
        "release_year": 2000,
        "poster_url": "https://image.tmdb.org/t/p/w500/m8FsNsDvs2KU9GgiyY5Ghrj9hkx.jpg"
    },
    {
        "title": "Superbad: É Hoje",
        "synopsis": "Dois amigos adolescentes do ensino médio tentam comprar bebidas para uma grande festa de formatura, mas seus planos dão terrivelmente errado.",
        "category": "Comédia",
        "release_year": 2007,
        "poster_url": "https://image.tmdb.org/t/p/w500/ek8e8txUyUvd2BNqj6UFE59jgvg.jpg"
    },

    # SÉRIES DE TV
    {
        "title": "Breaking Bad",
        "synopsis": "Um professor de química do ensino médio diagnosticado com câncer terminal de pulmão se volta para a fabricação de metanfetamina com um ex-aluno.",
        "category": "Séries",
        "release_year": 2008,
        "poster_url": "https://image.tmdb.org/t/p/w500/ztkUQFLlC19CCMYHW9o1zWhJRNq.jpg"
    },
    {
        "title": "Stranger Things",
        "synopsis": "Quando um jovem garoto desaparece, sua mãe, um xerife e seus amigos devem confrontar forças sobrenaturais aterrorizantes e experimentos secretos do governo.",
        "category": "Séries",
        "release_year": 2016,
        "poster_url": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg"
    },
    {
        "title": "The Last of Us",
        "synopsis": "Vinte anos após uma praga moderna destruir a civilização, Joel é contratado para contrabandear Ellie, uma jovem garota imune de 14 anos, para fora de uma zona de quarentena opressiva.",
        "category": "Séries",
        "release_year": 2023,
        "poster_url": "https://image.tmdb.org/t/p/w500/uKvVjK19u7vgRecSt2nbv99umao.jpg"
    },
    {
        "title": "Dark",
        "synopsis": "O desaparecimento de duas crianças em uma cidade alemã expõe os relacionamentos fraturados entre quatro famílias e uma teia de viagens no tempo de várias gerações.",
        "category": "Séries",
        "release_year": 2017,
        "poster_url": "https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg"
    },
    {
        "title": "Succession",
        "synopsis": "A família Roy é conhecida por controlar a Waystar RoyCo, um dos maiores conglomerados de mídia e entretenimento do mundo. Quando o patriarca decide se afastar, uma disputa pelo poder se inicia.",
        "category": "Séries",
        "release_year": 2018,
        "poster_url": "https://image.tmdb.org/t/p/w500/7udWdOqUqXpPjM9f7VlD4lDk1iK.jpg"
    }
]

def run_seed():
    print("Iniciando Seed no Supabase...")

    # 1. Popula Usuários
    print("\n1. Populando Usuários (Alunos e Contas de Teste)...")
    user_records = []
    for u in USERS_SEED:
        hashed = hash_password(u["password"])
        user_records.append({
            "name": u["name"],
            "email": u["email"].lower().strip(),
            "password_hash": hashed
        })

    try:
        # Upsert baseado no email unique
        res_users = supabase.table("users").upsert(
            user_records,
            on_conflict="email"
        ).execute()
        print(f"   {len(res_users.data or user_records)} usuários garantidos no banco!")
    except Exception as e:
        print(f"   Erro ao inserir usuários: {e}")
        return False

    # 2. Popula Itens (Catálogo de Obras)
    print("\n2. Populando Catálogo de Obras...")
    try:
        # Checa quantos itens já existem para não duplicar se rodar de novo
        check_items = supabase.table("items").select("id, title").execute()
        existing_titles = {item["title"] for item in (check_items.data or [])}

        items_to_insert = [
            item for item in ITEMS_SEED if item["title"] not in existing_titles
        ]

        if items_to_insert:
            res_items = supabase.table("items").insert(items_to_insert).execute()
            print(f"   {len(res_items.data or items_to_insert)} novas obras cadastradas com sucesso!")
        else:
            print("   Obras já constavam no banco de dados.")
    except Exception as e:
        print(f"   Erro ao inserir obras: {e}")
        return False

    # 3. Popula algumas avaliações iniciais para enriquecer os testes
    print("\n3. Criando avaliações iniciais de exemplo...")
    try:
        all_users = supabase.table("users").select("id, email").execute().data or []
        all_items = supabase.table("items").select("id, title").limit(6).execute().data or []

        if all_users and all_items:
            u_id = all_users[0]["id"]
            reviews_sample = [
                {"user_id": u_id, "item_id": all_items[0]["id"], "rating": 5, "comment": "Obra de arte absoluta!"},
                {"user_id": u_id, "item_id": all_items[1]["id"], "rating": 5, "comment": "Excelente trilha sonora e atuações."},
            ]
            if len(all_users) > 1 and len(all_items) > 2:
                u2_id = all_users[1]["id"]
                reviews_sample.append({"user_id": u2_id, "item_id": all_items[0]["id"], "rating": 4, "comment": "Muito bom, recomendo."})
                reviews_sample.append({"user_id": u2_id, "item_id": all_items[2]["id"], "rating": 5, "comment": "Simplesmente imperdível."})

            supabase.table("reviews").upsert(reviews_sample, on_conflict="user_id,item_id").execute()
            print(f"   {len(reviews_sample)} avaliações iniciais registradas!")
    except Exception as e:
        print(f"   Aviso ao criar avaliações iniciais: {e}")

    print("\n Seed concluído com sucesso!")
    print("Contas disponíveis para teste:")
    for u in USERS_SEED:
        print(f"   - {u['email']} | Senha: {u['password']} ({u['name']})")
    return True

if __name__ == "__main__":
    success = run_seed()
    sys.exit(0 if success else 1)
