<template>
  <main class="flex-grow">
    <div class="flex flex-col gap-2 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Over Signal Jam</h2>
    </div>

    <div class="space-y-4 max-w-3xl">
      <p class="text-sm text-gray-700 leading-relaxed">
      Binnen het project Signal Jam doen journalisten en programmeurs van het collectief Open Eyes onderzoek naar de verspreiding van desinformatie rondom de oorlog in Oekraïne. De artikelen die we schrijven op basis van de gevonden data publiceren we <a href="https://smallstreammedia.nl/dossiers/cross-border-onderzoek/signal-jam/" class="underline">hier.</a>
      </p>
      <p class="text-sm text-gray-700 leading-relaxed">
        Het dashboard dat je hier ziet, is het hart van dit onderzoek. We verzamelen hier posts die bepaalde termen bevatten of zijn geplaatst door bekende verspreiders van (pro-Russische) desinformatie. We analyseren alleen posts in het Nederlands, we richten ons immers op het Nederlandse taalgebied. Alle posts zijn met de hand gecontroleerd voordat ze het label "desinformatie" krijgen. Daarbij maken we vooral gebruik van factchecks en eerder onderzoek naar desinformatie-frames. 
      </p>
      <p class="text-sm text-gray-700 leading-relaxed">
        Er zijn twee manieren waarop een post in dit dashboard terecht kan komen. Allereerst zoeken we naar posts met daarin termen die vaak voorkomen in pro-Russische desinformatie, en naar posts die links bevatten van bekende propagandakanalen zoals RT en sites uit het Pravda-netwerk. Daarnaast zoeken we naar accounts die vaker (minstens drie keer) pro-Russische desinformatie hebben verspreid, waarna al hun posts in deze database terechtkomen. Let op: alleen de posts met het label "Bevat desinformatie" zijn met de hand gecontroleerd op desinformatie.
      </p>
      <p class="text-sm text-gray-700 leading-relaxed">
        De artikelen zijn verzameld via bekende desinformatiekanalen die (indirect) onder controle staan van het Kremlin. Denk aan Lenta, RT en grote desinformatienetwerken zoals het Pravda-netwerk. Vanwege de hoeveelheid desinformatie in deze artikelen, hebben we ze wel achter een wachtwoord gezet. Wat erin staat, kun je ook terugvinden in de samenvattingen.
      </p>
      <p class="text-sm text-gray-700 leading-relaxed">
      De code van het dashboard is <em>open source</em>, je kunt deze zelf ook draaien. <a target="_blank" href="https://github.com/jorisheijkant/signal-jam" class="underline">De code is beschikbaar via Github</a>.
      </p>
      <p class="text-sm text-gray-700 font-bold leading-relaxed">
        Dit onderzoek is mede mogelijk gemaakt door
      </p>
      <div class="flex flex-wrap items-center gap-8 py-2">
        <a href="https://sdm.nl/" target="_blank" rel="noopener" class="opacity-80 hover:opacity-100 transition-opacity">
          <img src="/logos/sdm_logo.png" alt="SDM" class="h-10 w-auto object-contain" />
        </a>
        <a href="https://www.sidnfonds.nl/" target="_blank" rel="noopener" class="opacity-80 hover:opacity-100 transition-opacity">
          <img src="/logos/sidn_logo.png" alt="SIDN" class="h-10 w-auto object-contain" />
        </a>
        <a href="https://verspers.nl/" target="_blank" rel="noopener" class="opacity-80 hover:opacity-100 transition-opacity">
          <img src="/logos/verspers_logo.png" alt="Verspers" class="h-10 w-auto object-contain" />
        </a>
        <a href="https://www.vfonds.nl/" target="_blank" rel="noopener" class="opacity-80 hover:opacity-100 transition-opacity">
          <img src="/logos/vfonds_logo.png" alt="VFonds" class="h-10 w-auto object-contain" />
        </a>
      </div>
    </div>
  </main>
</template>
