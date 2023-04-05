// Resume.js
import React, {useState} from 'react';

function Resume() {

    const [alignment] = useState("left");

    return (
        <div>
            <h1 className="font-link">Resume</h1>
            <hr
                style={{
                    background: "#808080",
                    height: "2px",
                    border: "none",
                }}
            />
            <h3 className="font-link">Education: </h3>
            <div align={alignment} className="font-link">
                ● Columbia University, Graduate School of Arts and Sciences<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;August 2022 - December 2023</em>
                <ul>
                    <li>Master of Arts in Quantitative Methods in the Social Sciences</li>
                    <li>Specialization in data science with a focus on sports analytics and machine learning</li>
                </ul>
                ● Columbia University, Columbia College<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;August 2017 - April 2021</em>
                <ul>
                    <li>Bachelor of Arts: Major in English Literature, minor in Computer Science</li>
                    <li>Placement on the Dean’s List for highly commended students</li>
                </ul>
            </div>
            <h3 className="font-link">Professional Experience: </h3>
            <div align={alignment} className='font-link'>
                ● Data Analyst Intern: Penelope<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;February 2023 - Present</em>
                <ul>
                    <li>Designed and implemented a conversion marketing accelerator in python, with automated data collection
                    and cleaning. With this new tool, the company achieved 25% growth in client acquisition</li>
                    <li>Provided in-depth analytics reporting on marketing efficacy, using a range of tools such as
                    A/B testing, generative probability modeling, logistic regression and random forrest </li>
                    <li>Built an interactive dashboard in Tableau that provides data insights and live updates on
                        marketing progress, to be used by all company personnel
                    </li>
                </ul>
                ● Data Analyst: Équilibre Biopharmaceuticals Corp<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;August 2022 - December 2022</em>
                <ul>
                    <li>Worked with the biostatistics team to conduct in-depth analysis on various data sets from
                        Équilibre’s phase 1 and phase 2 studies</li>
                    <li>Utilized R and Java-based programming to produce a range of models in support of literature writing
                        and correspondence with the FDA</li>
                    <li>Implemented a standardized protocol for peer-reviewing tasks, which improved the accuracy of
                        subsequent code testing by 35%</li>
                </ul>
                ● Associate Director of Data Management: Équilibre Biopharmaceuticals Corp<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;August 2021 - August 2022</em>
                <ul>
                    <li>Built and maintained an in-house database for a series of clinical trials in phases 2 and 3 of drug
                        candidate development</li>
                    <li>Reported data management and biostatistics takeaways to stakeholders on a weekly basis</li>
                    <li>Created a range of automated processes to improve the efficiency of data management and data cleaning
                        operations by 40%</li>
                </ul>
                ● Associate Consultant Intern: Konrad Group<br/>
                &nbsp;&nbsp;&nbsp;New York, NY, USA<br/>
                <em>&nbsp;&nbsp;&nbsp;May - August 2020</em>
                <ul>
                    <li>Worked closely with a team of software developers and cloud computing specialists to create
                        digital solutions for a variety of clients</li>
                    <li>Supported the team in understanding our client’s business challenges, acting as the bridge between
                        consultants and developers</li>
                    <li>Structured presentations, documentation, requests for proposal responses, and other collateral</li>
                </ul>
            </div>
            <h3 className="font-link">School and Collegiate Athletics: </h3>
            <div align={alignment} className='font-link'>
                ● Men's Varsity Rowing: Eton College<br/>
                <ul>
                    <li>One gold and one silver medal at the Schools Head of the River Race</li>
                    <li>Three gold and two silver medals at the British National Schools Regatta</li>
                    <li>Semi-finalist at Henley Royal Regatta (Princess Elizabeth Challenge Cup, 2017)</li>
                </ul>
                ● Men's Varsity Rowing: Columbia University<br/>
                <ul>
                    <li>Represented my university as a senior member of the team and dedicated over 30 hours a week to
                        training and competing</li>
                    <li>Frequently hosted potential recruits during their official visits to the university</li>
                </ul>
                ● Other:<br/>
                <ul>
                    <li>2022 IronMan Ireland 70.3, finisher (7th/180 in the 18-24 male category)</li>
                </ul>
            </div>
        </div>
    );
}

export default Resume;