import { ArrowRight, Check } from "lucide-react";
import {
  motion,
  useInView,
  useScroll,
  useTransform,
  type MotionValue
} from "framer-motion";
import { useMemo, useRef } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;
const cardEase = [0.22, 1, 0.36, 1] as const;

const heroVideo =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_170732_8a9ccda6-5cff-4628-b164-059c500a2b41.mp4";
const cardVideo =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260406_133058_0504132a-0cf3-4450-a370-8ea3b05c95d4.mp4";

type Segment = {
  text: string;
  className?: string;
};

type AnimatedLetterProps = {
  char: string;
  index: number;
  total: number;
  progress: MotionValue<number>;
};

function WordsPullUp({
  text,
  showAsterisk = false,
  className = ""
}: {
  text: string;
  showAsterisk?: boolean;
  className?: string;
}) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true });
  const words = text.split(" ");

  return (
    <span ref={ref} className={className}>
      {words.map((word, index) => (
        <span className="inline-block overflow-hidden" key={`${word}-${index}`}>
          <motion.span
            className="relative inline-block"
            initial={{ y: 20 }}
            animate={isInView ? { y: 0 } : { y: 20 }}
            transition={{ duration: 0.9, delay: index * 0.08, ease: easeOut }}
          >
            {word}
            {showAsterisk && index === words.length - 1 ? (
              <span className="absolute top-[0.65em] -right-[0.3em] text-[0.31em]">*</span>
            ) : null}
            {index < words.length - 1 ? "\u00a0" : ""}
          </motion.span>
        </span>
      ))}
    </span>
  );
}

function WordsPullUpMultiStyle({
  segments,
  className = ""
}: {
  segments: Segment[];
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });
  const words = useMemo(() => {
    const result: Array<{ word: string; className?: string }> = [];
    segments.forEach((segment) => {
      segment.text.split(" ").forEach((word) => {
        result.push({ word, className: segment.className });
      });
    });
    return result;
  }, [segments]);

  return (
    <div ref={ref} className={`inline-flex flex-wrap justify-center ${className}`}>
      {words.map(({ word, className: wordClassName }, index) => (
        <span className="inline-block overflow-hidden" key={`${word}-${index}`}>
          <motion.span
            className={`inline-block ${wordClassName ?? ""}`}
            initial={{ y: 20 }}
            animate={isInView ? { y: 0 } : { y: 20 }}
            transition={{ duration: 0.9, delay: index * 0.08, ease: easeOut }}
          >
            {word}
            {index < words.length - 1 ? "\u00a0" : ""}
          </motion.span>
        </span>
      ))}
    </div>
  );
}

function AnimatedLetter({ char, index, total, progress }: AnimatedLetterProps) {
  const charProgress = index / total;
  const opacity = useTransform(progress, [charProgress - 0.1, charProgress + 0.05], [0.2, 1]);
  return <motion.span style={{ opacity }}>{char}</motion.span>;
}

function ScrollRevealText({ text }: { text: string }) {
  const ref = useRef<HTMLParagraphElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.8", "end 0.2"]
  });
  const letters = Array.from(text);

  return (
    <p ref={ref} className="mx-auto mt-10 max-w-2xl text-xs leading-relaxed text-[#DEDBC8] sm:text-sm md:text-base">
      {letters.map((char, index) => (
        <AnimatedLetter
          char={char}
          index={index}
          total={letters.length}
          progress={scrollYProgress}
          key={`${char}-${index}`}
        />
      ))}
    </p>
  );
}

function FeatureCard({
  index,
  title,
  icon,
  items
}: {
  index: string;
  title: string;
  icon: string;
  items: string[];
}) {
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.article
      ref={ref}
      className="flex min-h-[360px] flex-col bg-[#212121] p-5 sm:min-h-[420px] sm:p-6 lg:h-[480px]"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.7, delay: Number(index) * 0.15, ease: cardEase }}
    >
      <img className="h-10 w-10 rounded object-cover sm:h-12 sm:w-12" src={icon} alt="" />
      <div className="mt-10 flex items-start justify-between gap-4">
        <h3 className="text-xl leading-none text-[#E1E0CC] sm:text-2xl">{title}</h3>
        <span className="text-xs text-gray-500">{index.padStart(2, "0")}</span>
      </div>
      <ul className="mt-9 space-y-4">
        {items.map((item) => (
          <li className="flex gap-3 text-sm leading-tight text-gray-400" key={item}>
            <Check className="mt-[1px] h-4 w-4 shrink-0 text-primary" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
      <a className="mt-auto inline-flex items-center gap-2 pt-8 text-sm text-primary" href="#about">
        Mehr erfahren
        <ArrowRight className="h-4 w-4 -rotate-45" />
      </a>
    </motion.article>
  );
}

function VideoFeatureCard() {
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.article
      ref={ref}
      className="relative min-h-[360px] overflow-hidden sm:min-h-[420px] lg:h-[480px]"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.7, ease: cardEase }}
    >
      <video className="absolute inset-0 h-full w-full object-cover" src={cardVideo} autoPlay loop muted playsInline />
      <p className="absolute bottom-6 left-6 z-10 max-w-[12rem] text-xl leading-none text-[#E1E0CC] sm:text-2xl">
        Dein kreativer Abdruck.
      </p>
    </motion.article>
  );
}

function Hero() {
  return (
    <section className="h-screen p-4 md:p-6" data-prompt-id="prisma-landing" aria-label="Fotoecke Rheine">
      <div className="relative h-full overflow-hidden rounded-2xl bg-black md:rounded-[2rem]">
        <video className="absolute inset-0 h-full w-full object-cover" src={heroVideo} autoPlay loop muted playsInline />
        <div className="noise-overlay pointer-events-none absolute inset-0 opacity-[0.7] mix-blend-overlay" />
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/60" />

        <nav className="absolute left-1/2 top-0 z-20 flex -translate-x-1/2 gap-3 rounded-b-2xl bg-black px-4 py-2 sm:gap-6 md:gap-12 md:rounded-b-3xl md:px-8 lg:gap-14">
          {["Passbilder", "Portraits", "Bewerbung", "Rahmen", "Kontakt"].map((item) => (
            <a
              className="text-[10px] transition-colors sm:text-xs md:text-sm"
              href={item === "Kontakt" ? "#features" : "#about"}
              style={{ color: "rgba(225, 224, 204, 0.8)" }}
              onMouseEnter={(event) => {
                event.currentTarget.style.color = "#E1E0CC";
              }}
              onMouseLeave={(event) => {
                event.currentTarget.style.color = "rgba(225, 224, 204, 0.8)";
              }}
              key={item}
            >
              {item}
            </a>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 z-10 grid grid-cols-12 items-end gap-4 px-4 pb-4">
          <h1
            className="col-span-12 m-0 text-[24vw] font-medium leading-[0.85] tracking-[-0.07em] text-[#E1E0CC] sm:text-[22vw] md:col-span-8 md:text-[19vw] lg:text-[17vw] xl:text-[16vw] 2xl:text-[17vw]"
          >
            <WordsPullUp text="Fotoecke" showAsterisk />
          </h1>
          <div className="col-span-12 flex max-w-lg flex-col items-start gap-5 pb-4 md:col-span-4">
            <motion.p
              className="text-xs leading-[1.2] text-primary/70 sm:text-sm md:text-base"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.5, ease: easeOut }}
            >
              Fotoecke Rheine ist ein lokaler Ort fuer E-Passbilder, Bewerbungsfotos und
              Portraits, getragen von Erfahrung, Sorgfalt und dem Blick fuer Bilder, die direkt
              funktionieren.
            </motion.p>
            <motion.a
              className="group inline-flex items-center gap-2 rounded-full bg-primary py-1 pl-5 pr-1 text-sm font-medium text-black transition-all hover:gap-3 sm:text-base"
              href="tel:+49597117080"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, delay: 0.7, ease: easeOut }}
            >
              Jetzt anrufen
              <span className="grid h-9 w-9 place-items-center rounded-full bg-black transition-transform group-hover:scale-110 sm:h-10 sm:w-10">
                <ArrowRight className="h-4 w-4 text-[#E1E0CC]" />
              </span>
            </motion.a>
          </div>
        </div>
      </div>
    </section>
  );
}

function About() {
  return (
    <section id="about" className="bg-black px-4 py-24" data-prompt-id="prisma-landing">
      <div className="mx-auto max-w-6xl bg-[#101010] px-6 py-20 text-center">
        <p className="mb-6 text-[10px] text-primary sm:text-xs">Fotoatelier</p>
        <h2 className="mx-auto max-w-3xl text-3xl font-normal leading-[0.95] text-[#E1E0CC] sm:text-4xl sm:leading-[0.9] md:text-5xl lg:text-6xl xl:text-7xl">
          <WordsPullUpMultiStyle
            segments={[
              { text: "Wir sind Fotoecke," },
              { text: "ein Studio in Rheine.", className: "font-serif italic" },
              { text: "Passbilder, Portraits, Bewerbung und Rahmen." }
            ]}
          />
        </h2>
        <ScrollRevealText text="Seit Jahren begleitet Fotoecke Rheine Menschen, die schnell ein rechtskonformes Ausweisfoto brauchen, ein starkes Bewerbungsbild suchen oder ein persoenliches Portrait verschenken moechten. Im Laden entstehen digitale E-Passbilder, Ausdrucke, Dateien, Alben und Rahmen mit ruhiger Beratung." />
      </div>
    </section>
  );
}

function Features() {
  const icon1 =
    "https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171918_4a5edc79-d78f-4637-ac8b-53c43c220606.png&w=1280&q=85";
  const icon2 =
    "https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171741_ed9845ab-f5b2-4018-8ce7-07cc01823522.png&w=1280&q=85";
  const icon3 =
    "https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171809_f56666dc-c099-4778-ad82-9ad4f209567b.png&w=1280&q=85";

  return (
    <section id="features" className="bg-noise min-h-screen bg-black px-4 py-24" data-prompt-id="prisma-landing">
      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="mb-12 text-center text-xl font-normal sm:text-2xl md:text-3xl lg:text-4xl">
          <WordsPullUpMultiStyle
            segments={[
              { text: "Studio-Ablaeufe fuer Bilder, die sofort sitzen.", className: "text-[#E1E0CC]" },
              { text: "Gebaut fuer Vertrauen. Gemacht fuer Rheine.", className: "text-gray-500" }
            ]}
          />
        </div>

        <div className="grid gap-3 sm:gap-2 md:grid-cols-2 md:gap-1 lg:grid-cols-4 lg:h-[480px]">
          <VideoFeatureCard />
          <FeatureCard
            index="1"
            title="E-Passbilder."
            icon={icon1}
            items={[
              "Biometrische Aufnahme nach aktuellen Vorgaben",
              "Digitale Uebermittlung an das Buergeramt",
              "Ausdrucke direkt zum Mitnehmen",
              "Passbild-Garantie bei Ablehnung"
            ]}
          />
          <FeatureCard
            index="2"
            title="Bewerbungsfotos."
            icon={icon2}
            items={[
              "Auswahl direkt am Bildschirm",
              "Professioneller Ausdruck fuer Bewerbungsmappen",
              "Dateien auf CD oder USB-Stick"
            ]}
          />
          <FeatureCard
            index="3"
            title="Portrait & Rahmen."
            icon={icon3}
            items={[
              "Familien-, Kinder- und Business-Portraits",
              "Fotoalben fuer besondere Anlaesse",
              "Bilderrahmen und Passepartouts im Laden"
            ]}
          />
        </div>
      </div>
    </section>
  );
}

export default function App() {
  return (
    <main>
      <Hero />
      <About />
      <Features />
    </main>
  );
}
