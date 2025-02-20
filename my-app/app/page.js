import Image from "next/image";
import "./page.module.css";
import Link from "next/link";
import Card from "@/Components/Card";

export default function Home() {
  const cardsData = [
    { title: "Personalized Learning", content: "Leverages LLMs & ML to create dynamic, adaptive study plans tailored to each student’s strengths, weaknesses, and available time. AI-driven schedules adapt to each student’s strengths, weaknesses, and available time, ensuring efficient study plans."},
    { title: "Positive Student Impact", content: "We expect students to study better and get better grades with LearnSphere. It helps them manage time and focus on weak areas, leading to academic success." },
    { title: "Seamless Organization", content: "Google Calendar integration reduces stress, helping students manage their workload effectively and build better study habits. We plan to add features like adaptive learning and games to make studying more fun and effective, further enhancing the platform's impact. " }
  ];
  return (
    <div className="landing-page">
      <div className="box">
        <div className="title">Plan. Learn. Achieve</div>
        <div className="content">Stay organized and make the most of your study time with LearnSphere. Effortlessly schedule your tasks, track progress, and stay ahead in your academic journey. Your smart study planner, designed for success!</div>
      </div>
      
      <Link href={"/Feature"}><button className="button-33" role="button">Start Planning</button></Link>

      <div className="box">
        <div className="cards">
          {cardsData.map((card, index) => (
            <Card key={index} title={card.title} content={card.content} />
          ))}
        </div>
      </div>

    </div>
  );
}
