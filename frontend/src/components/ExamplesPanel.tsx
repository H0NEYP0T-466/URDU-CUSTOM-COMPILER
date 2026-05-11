import "./ExamplesPanel.css";

interface Example {
  title: string;
  icon: string;
  description: string;
  code: string;
}

const EXAMPLES: Example[] = [
  {
    title: "Hello World",
    icon: "👋",
    description: "Pehla program -- screen pe message dikhao",
    code: `dikhao "Assalam o Alaikum Duniya!"
dikhao "Yeh meri pehli Urdu program hai"`,
  },
  {
    title: "If / Else",
    icon: "🔀",
    description: "Agar-warna se condition check karo",
    code: `rakho x = 10
rakho y = 3
agar x > y
    dikhao "x bara hai"
warna
    dikhao "y bara hai"
khatam`,
  },
  {
    title: "While Loop Counter",
    icon: "🔄",
    description: "Jabtak loop se ginti karo",
    code: `rakho x = 5
jabtak x > 0
    dikhao x
    rakho x = x - 1
khatam
dikhao "Ulti ginti khatam!"`,
  },
  {
    title: "Arithmetic",
    icon: "🧮",
    description: "Numbers ke saath hisaab karo",
    code: `rakho a = 15
rakho b = 4
rakho jama = a + b
rakho minus = a - b
rakho zarb = a * b
rakho taqseem = a / b
dikhao "Jama: "
dikhao jama
dikhao "Minus: "
dikhao minus
dikhao "Zarb: "
dikhao zarb
dikhao "Taqseem: "
dikhao taqseem`,
  },
  {
    title: "Constant Folding",
    icon: "⚡",
    description: "Optimizer constants ko compile-time pe calculate karega",
    code: `# Yeh values compile-time pe fold ho jayengi
rakho x = 5 + 3
rakho y = 10 * 2
rakho z = 100 / 4
rakho w = 50 - 15
dikhao "x = "
dikhao x
dikhao "y = "
dikhao y
dikhao "z = "
dikhao z
dikhao "w = "
dikhao w
dikhao "Sab kuch compile-time pe calculate hua!"`,
  },
  {
    title: "Const Propagation",
    icon: "🔗",
    description: "Optimizer variables ko unki values se replace karega",
    code: `# a aur b sirf ek baar assign hote hain
# optimizer inhe directly value se replace karega
rakho a = 7
rakho b = 3
rakho result = a + b
rakho diff = a - b
rakho product = a * b
dikhao "Result: "
dikhao result
dikhao "Difference: "
dikhao diff
dikhao "Product: "
dikhao product`,
  },
  {
    title: "Boolean Logic",
    icon: "🔘",
    description: "Sahi/ghalat aur logic operators test karo",
    code: `rakho x = 10
rakho y = 5
rakho check1 = x > 3 aur y < 20
rakho check2 = x == 5 ya y == 5
dikhao "x > 3 aur y < 20:"
dikhao check1
dikhao "x == 5 ya y == 5:"
dikhao check2
agar check1 aur check2
    dikhao "Dono sahi hain!"
khatam`,
  },
  {
    title: "Semantic Error",
    icon: "🚨",
    description: "Semantic analyzer ghaltiyan pakrega",
    code: `# Yeh code mein jaanboojh kar ghaltiyan hain
# Semantic analyzer inhe catch karega
rakho x = "hello"
rakho y = x + 5
dikhao z`,
  },
  {
    title: "Functions",
    icon: "🔧",
    description: "banao se function define karo, karo se call karo",
    code: `# Function banao aur use karo
banao add(a, b)
    wapis a + b
khatam

banao greet(naam)
    dikhao "Assalam o Alaikum, "
    dikhao naam
khatam

karo greet("Duniya")
rakho result = add(10, 20)
dikhao "Jama: "
dikhao result`,
  },
  {
    title: "Arrays",
    icon: "📋",
    description: "Lists banao, access karo, aur modify karo",
    code: `# Array/List banana aur use karna
rakho fruits = ["Aam", "Seb", "Kela"]
dikhao fruits[0]
dikhao fruits[1]
dikhao fruits[2]

# Array value change karo
rakho fruits[1] = "Anaar"
dikhao "Update ke baad:"
dikhao fruits[1]

# Numbers ki list
rakho nums = [10, 20, 30, 40, 50]
rakho total = nums[0] + nums[1] + nums[2]
dikhao "Pehle 3 ka total: "
dikhao total`,
  },
  {
    title: "User Input",
    icon: "⌨️",
    description: "User se input lo aur use karo (neeche input do)",
    code: `# User se naam lo
rakho naam = input("Apna naam likho: ")
dikhao "Assalam o Alaikum, "
dikhao naam

# Number input lo aur double karo
rakho x = int(input("Ek number likho: "))
rakho double = x * 2
dikhao "Double: "
dikhao double`,
  },
];

interface ExamplesPanelProps {
  isOpen: boolean;
  onSelectExample: (code: string) => void;
}

export default function ExamplesPanel({ isOpen, onSelectExample }: ExamplesPanelProps) {
  return (
    <aside
      className={`examples-panel ${isOpen ? "" : "examples-panel--collapsed"}`}
      id="examples-panel"
    >
      <div className="examples-panel__header">
        <h2 className="examples-panel__title">Misaalein</h2>
      </div>
      <div className="examples-panel__list">
        {EXAMPLES.map((example, index) => (
          <button
            key={index}
            className="examples-panel__card"
            onClick={() => onSelectExample(example.code)}
            id={`example-card-${index}`}
          >
            <div className="examples-panel__card-icon">{example.icon}</div>
            <div className="examples-panel__card-title">{example.title}</div>
            <div className="examples-panel__card-desc">{example.description}</div>
          </button>
        ))}
      </div>
    </aside>
  );
}
