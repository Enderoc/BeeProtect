from http.server import BaseHTTPRequestHandler
from flask import Flask, render_template_string

# ВАЖНО: Создаем приложение ОДИН раз вне функции
app = Flask(__name__)
common_style = '''
<style>
    :root {
        --primary-yellow: #FFD700;
        --secondary-yellow: #FFC107;
        --dark-yellow: #FFA000;
        --light-yellow: #FFF9C4;
        --dark-bg: #1A1A1A;
        --card-bg: #2D2D2D;
        --text-light: #FFFFFF;
        --text-gray: #B0B0B0;
        --accent-green: #4CAF50;
        --accent-blue: #2196F3;
        --accent-orange: #FF9800;
        --accent-purple: #9C27B0;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--dark-bg);
        color: var(--text-light);
        line-height: 1.6;
        overflow-x: hidden;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    /* Navigation */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(26, 26, 26, 0.95);
        backdrop-filter: blur(10px);
        z-index: 1000;
        padding: 15px 0;
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
    }

    .nav-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }

    .nav-logo-icon {
        font-size: 1.8rem;
        color: var(--primary-yellow);
    }

    .nav-logo-text {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nav-links {
        display: flex;
        gap: 30px;
    }

    .nav-link {
        color: var(--text-gray);
        text-decoration: none;
        font-weight: 500;
        font-size: 1rem;
        padding: 8px 16px;
        border-radius: 20px;
        transition: all 0.3s ease;
        position: relative;
    }

    .nav-link:hover {
        color: var(--text-light);
        background: rgba(255, 215, 0, 0.1);
    }

    .nav-link.active {
        color: var(--primary-yellow);
        background: rgba(255, 215, 0, 0.15);
    }

    .nav-link.active::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 3px;
        background: var(--primary-yellow);
        border-radius: 2px;
    }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, rgba(26,26,26,0.9) 0%, rgba(45,45,45,0.8) 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        position: relative;
        padding: 120px 0 80px;
        margin-top: 60px;
    }

    .hero::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 150px;
        background: linear-gradient(to bottom, transparent, var(--dark-bg));
    }

    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
        max-width: 900px;
        margin: 0 auto;
    }

    .logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
    }

    .logo-icon {
        font-size: 5rem;
        color: var(--primary-yellow);
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        line-height: 1.1;
    }

    .tagline {
        font-size: 1.5rem;
        color: var(--text-gray);
        max-width: 800px;
        margin: 0 auto 40px;
    }

    .cta-button {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange));
        color: var(--dark-bg);
        padding: 15px 40px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        margin-top: 20px;
    }

    .cta-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255, 215, 0, 0.3);
    }

    /* Section Common */
    .section {
        padding: 100px 0;
    }

    .section-title {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        margin-bottom: 60px;
        color: var(--text-light);
    }

    .highlight {
        color: var(--primary-yellow);
    }

    /* Mission Cards */
    .mission-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 50px;
    }

    .mission-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }

    .mission-card:hover {
        transform: translateY(-10px);
        border-color: var(--primary-yellow);
    }

    .mission-icon {
        font-size: 3rem;
        color: var(--primary-yellow);
        margin-bottom: 20px;
    }

    .mission-card h3 {
        font-size: 1.5rem;
        margin-bottom: 15px;
        color: var(--text-light);
    }

    /* Goals Grid */
    .goals-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
    }

    .goal-item {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 30px;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: all 0.3s ease;
    }

    .goal-item:hover {
        background: rgba(255, 215, 0, 0.1);
    }

    .goal-number {
        background: var(--primary-yellow);
        color: var(--dark-bg);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    /* Team Section */
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 40px;
        margin-top: 50px;
    }

    .team-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .team-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .member-avatar {
        width: 150px;
        height: 150px;
        background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange));
        border-radius: 50%;
        margin: 0 auto 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        color: var(--dark-bg);
    }

    .member-name {
        font-size: 1.8rem;
        margin-bottom: 10px;
        color: var(--text-light);
    }

    .member-role {
        color: var(--primary-yellow);
        font-size: 1.1rem;
        margin-bottom: 20px;
        font-weight: 500;
    }

    .member-bio {
        color: var(--text-gray);
        line-height: 1.7;
    }

    /* Stats */
    .stats {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        margin: 40px 0;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: block;
    }

    .stat-label {
        color: var(--text-gray);
        font-size: 0.9rem;
        margin-top: 10px;
    }

    /* Tech Stack */
    .tech-stack {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 25px;
        margin-top: 50px;
    }

    .tech-item {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .tech-item:hover {
        transform: translateY(-5px);
        border: 1px solid var(--primary-yellow);
    }

    .tech-icon {
        font-size: 3rem;
        color: var(--primary-yellow);
        margin-bottom: 20px;
    }

    /* Footer */
    footer {
        background: var(--card-bg);
        padding: 60px 0 30px;
        text-align: center;
        border-top: 1px solid rgba(255, 215, 0, 0.1);
    }

    .footer-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
    }

    .social-links {
        display: flex;
        gap: 20px;
        margin: 20px 0;
    }

    .social-link {
        width: 50px;
        height: 50px;
        background: var(--dark-bg);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary-yellow);
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }

    .social-link:hover {
        background: var(--primary-yellow);
        color: var(--dark-bg);
        transform: translateY(-5px);
    }

    .copyright {
        color: var(--text-gray);
        font-size: 0.9rem;
        margin-top: 30px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .nav-links {
            gap: 10px;
        }

        .nav-link {
            padding: 6px 12px;
            font-size: 0.9rem;
        }

        h1 {
            font-size: 2.5rem;
        }

        .tagline {
            font-size: 1.2rem;
        }

        .logo-icon {
            font-size: 3rem;
        }

        .section {
            padding: 60px 0;
        }

        .section-title {
            font-size: 2rem;
            margin-bottom: 40px;
        }

        .team-grid {
            grid-template-columns: 1fr;
        }
    }

    /* Scroll Animation */
    .fade-in {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease;
    }

    .fade-in.visible {
        opacity: 1;
        transform: translateY(0);
    }

    /* Timeline */
    .timeline {
        position: relative;
        max-width: 800px;
        margin: 50px auto;
    }

    .timeline::before {
        content: '';
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 100%;
        background: var(--primary-yellow);
    }

    .timeline-item {
        position: relative;
        margin-bottom: 50px;
        width: 50%;
    }

    .timeline-item:nth-child(odd) {
        left: 0;
        padding-right: 60px;
        text-align: right;
    }

    .timeline-item:nth-child(even) {
        left: 50%;
        padding-left: 60px;
    }

    .timeline-dot {
        position: absolute;
        width: 20px;
        height: 20px;
        background: var(--primary-yellow);
        border-radius: 50%;
        top: 10px;
    }

    .timeline-item:nth-child(odd) .timeline-dot {
        right: -10px;
    }

    .timeline-item:nth-child(even) .timeline-dot {
        left: -10px;
    }

    .timeline-content {
        background: var(--card-bg);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }

    .timeline-date {
        color: var(--primary-yellow);
        font-weight: 600;
        margin-bottom: 10px;
        display: block;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
'''

# JavaScript для анимаций
common_script = '''
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const fadeElements = document.querySelectorAll('.fade-in');
        const currentPath = window.location.pathname;

        // Подсветка активной навигации
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('href') === currentPath ||
                (currentPath === '/' && link.getAttribute('href') === '/company')) {
                link.classList.add('active');
            }
        });

        // Анимация появления при скролле
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(element => {
            observer.observe(element);
        });

        // Анимация статистики
        function animateStats() {
            const stats = document.querySelectorAll('.stat-number');
            if (stats.length > 0) {
                stats.forEach(stat => {
                    const target = parseInt(stat.textContent);
                    if (!isNaN(target)) {
                        let current = 0;
                        const increment = target / 30;
                        const timer = setInterval(() => {
                            current += increment;
                            if (current >= target) {
                                current = target;
                                clearInterval(timer);
                            }
                            stat.textContent = Math.round(current) + (stat.textContent.includes('%') ? '%' : '');
                        }, 50);
                    }
                });
            }
        }

        // Запускаем анимацию статистики, если есть элементы
        if (document.querySelectorAll('.stat-number').length > 0) {
            animateStats();
        }

        // Обработчик кнопок CTA
        document.querySelectorAll('.cta-button[data-scroll]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('data-scroll');
                document.getElementById(targetId)?.scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Обработчик формы контактов
        const contactButton = document.querySelector('.contact-form .cta-button');
        if (contactButton) {
            const emailInput = document.querySelector('.contact-input');
            contactButton.addEventListener('click', function(e) {
                e.preventDefault();
                if (emailInput && emailInput.value) {
                    alert('Спасибо за интерес к BeeProtect! Мы свяжемся с вами в ближайшее время.');
                    emailInput.value = '';
                } else {
                    alert('Пожалуйста, введите ваш email');
                }
            });
        }
    });
</script>
'''

# Шаблон для страницы "Команда/Компания"
company_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Наша команда | BeeProtect</title>
    {{ common_style }}
</head>
<body>
    <!-- Навигация -->
    <nav class="nav-container">
        <div class="container nav-content">
            <a href="/company" class="nav-logo">
                <i class="fas fa-bee nav-logo-icon"></i>
                <span class="nav-logo-text">BeeProtect</span>
            </a>
            <div class="nav-links">
                <a href="/company" class="nav-link">Наша команда</a>
                <a href="/project" class="nav-link">Наш проект</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="logo">
                    <i class="fas fa-users logo-icon"></i>
                </div>
                <h1>Наша команда</h1>
                <p class="tagline fade-in">
                    Молодые инноваторы, объединенные одной миссией — изменить будущее сельского хозяйства с помощью технологий
                </p>

                <div class="stats fade-in">
                    <div class="stat-item">
                        <span class="stat-number">5+</span>
                        <span class="stat-label">лет опыта в ИИ</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">100%</span>
                        <span class="stat-label">преданность делу</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">24/7</span>
                        <span class="stat-label">работаем над целью</span>
                    </div>
                </div>

                <button class="cta-button fade-in" data-scroll="mission">
                    <i class="fas fa-arrow-down"></i>
                    Узнать о нашей миссии
                </button>
            </div>
        </div>
    </section>

    <!-- Mission Section -->
    <section class="section" id="mission">
        <div class="container">
            <h2 class="section-title fade-in">Наша <span class="highlight">Миссия</span></h2>
            <p style="text-align: center; max-width: 800px; margin: 0 auto 50px; font-size: 1.2rem; color: var(--text-gray);" class="fade-in">
                Мы верим, что технологии могут изменить мир к лучшему. Наша миссия — защитить самых важных насекомых на планете и обеспечить устойчивое будущее сельского хозяйства.
            </p>

            <div class="mission-grid">
                <div class="mission-card fade-in">
                    <i class="fas fa-lightbulb mission-icon"></i>
                    <h3>Инновации</h3>
                    <p>Разрабатываем передовые решения на стыке ИИ и сельского хозяйства</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-handshake mission-icon"></i>
                    <h3>Сотрудничество</h3>
                    <p>Работаем с пчеловодами, учеными и технологическими компаниями</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-globe mission-icon"></i>
                    <h3>Воздействие</h3>
                    <p>Создаем решения, которые имеют реальное значение для экосистемы</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Team Section -->
    <section class="section" style="background: linear-gradient(135deg, var(--dark-bg) 0%, rgba(45,45,45,0.95) 100%);">
        <div class="container">
            <h2 class="section-title fade-in">Знакомьтесь с <span class="highlight">Командой</span></h2>

            <div class="team-grid">
                <div class="team-card fade-in">
                    <div class="member-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <h3 class="member-name">Амаль Махмутов</h3>
                    <p class="member-role">Основатель & Tech Lead</p>
                    <p class="member-bio">
                        Студент УУНИТ, разработчик ИИ-систем. Обладает глубокими знаниями в области машинного обучения и компьютерного зрения. Увлечен созданием технологий, которые решают реальные проблемы сельского хозяйства.
                    </p>
                </div>

                <div class="team-card fade-in">
                    <div class="member-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3 class="member-name">ИИ-Разработчики</h3>
                    <p class="member-role">Команда нейросетей</p>
                    <p class="member-bio">
                        Специалисты по машинному обучению и компьютерному зрению, работающие над созданием и обучением алгоритмов для анализа поведения пчел и ранней диагностики заболеваний.
                    </p>
                </div>

                <div class="team-card fade-in">
                    <div class="member-avatar">
                        <i class="fas fa-users-cog"></i>
                    </div>
                    <h3 class="member-name">Консультанты</h3>
                    <p class="member-role">Эксперты-пчеловоды</p>
                    <p class="member-bio">
                        Опытные пчеловоды и ученые, которые помогают нам понять реальные потребности и проблемы в пчеловодстве, обеспечивая практическую применимость наших решений.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Values Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title fade-in">Наши <span class="highlight">Ценности</span></h2>

            <div class="goals-grid">
                <div class="goal-item fade-in">
                    <div class="goal-number">01</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Инновации</h3>
                        <p style="color: var(--text-gray);">Постоянное совершенствование и внедрение новых технологий</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">02</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Качество</h3>
                        <p style="color: var(--text-gray);">Высокие стандарты во всем, что мы делаем</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">03</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Сотрудничество</h3>
                        <p style="color: var(--text-gray);">Работаем вместе для достижения общих целей</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">04</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Экологичность</h3>
                        <p style="color: var(--text-gray);">Заботимся о планете и ее экосистемах</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">05</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Обучение</h3>
                        <p style="color: var(--text-gray);">Постоянно развиваемся и учимся новому</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">06</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Ответственность</h3>
                        <p style="color: var(--text-gray);">Несем ответственность за результаты нашей работы</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Timeline -->
    <section class="section" style="background: linear-gradient(135deg, rgba(45,45,45,0.95) 0%, var(--dark-bg) 100%);">
        <div class="container">
            <h2 class="section-title fade-in">Наш <span class="highlight">Путь</span></h2>

            <div class="timeline">
                <div class="timeline-item fade-in">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-date">2023</span>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Идея</h3>
                        <p style="color: var(--text-gray);">Появление идеи использовать ИИ для мониторинга здоровья пчел после изучения проблем пчеловодства</p>
                    </div>
                </div>

                <div class="timeline-item fade-in">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-date">2024</span>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Исследования</h3>
                        <p style="color: var(--text-gray);">Глубокое изучение проблемы, анализ существующих решений, разработка концепции</p>
                    </div>
                </div>

                <div class="timeline-item fade-in">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-date">2025</span>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Разработка</h3>
                        <p style="color: var(--text-gray);">Создание прототипа системы, первые тесты и привлечение экспертов</p>
                    </div>
                </div>

                <div class="timeline-item fade-in">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-date">2026</span>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Внедрение</h3>
                        <p style="color: var(--text-gray);">Пилотные проекты на реальных пасеках, сбор обратной связи, масштабирование</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="logo">
                    <i class="fas fa-bee" style="font-size: 2rem; color: var(--primary-yellow);"></i>
                    <h2 style="background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2rem;">BeeProtect</h2>
                </div>

                <div class="nav-links">
                    <a href="/company" class="nav-link active">Наша команда</a>
                    <a href="/project" class="nav-link">Наш проект</a>
                </div>

                <p style="color: var(--text-gray); max-width: 600px; margin: 0 auto; text-align: center;">
                    Мы создаем будущее сельского хозяйства с помощью технологий искусственного интеллекта
                </p>

                <div class="social-links">
                    <a href="#" class="social-link">
                        <i class="fab fa-telegram"></i>
                    </a>
                    <a href="#" class="social-link">
                        <i class="fab fa-vk"></i>
                    </a>
                    <a href="https://github.com" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="mailto:amal-makhmutov@mail.ru" class="social-link">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>

                <p class="copyright">© 2024 BeeProtect. Все права защищены.</p>
            </div>
        </div>
    </footer>

    {{ common_script }}
</body>
</html>
'''

# Шаблон для страницы "Проект"
project_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Наш проект | BeeProtect</title>
    {{ common_style }}
</head>
<body>
    <!-- Навигация -->
    <nav class="nav-container">
        <div class="container nav-content">
            <a href="/company" class="nav-logo">
                <i class="fas fa-bee nav-logo-icon"></i>
                <span class="nav-logo-text">BeeProtect</span>
            </a>
            <div class="nav-links">
                <a href="/company" class="nav-link">Наша команда</a>
                <a href="/project" class="nav-link active">Наш проект</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="logo">
                    <i class="fas fa-bee logo-icon"></i>
                </div>
                <h1>Проект BeeProtect</h1>
                <p class="tagline fade-in">
                    Инновационная система мониторинга здоровья пчелосемей с использованием искусственного интеллекта и компьютерного зрения
                </p>

                <div class="stats fade-in">
                    <div class="stat-item">
                        <span class="stat-number">40%</span>
                        <span class="stat-label">снижение потерь</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">99%</span>
                        <span class="stat-label">точность ИИ</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">24/7</span>
                        <span class="stat-label">мониторинг</span>
                    </div>
                </div>

                <button class="cta-button fade-in" data-scroll="problem">
                    <i class="fas fa-arrow-down"></i>
                    Узнать о проблеме
                </button>
            </div>
        </div>
    </section>

    <!-- Problem Section -->
    <section class="section" id="problem">
        <div class="container">
            <h2 class="section-title fade-in">Проблема, которую <span class="highlight">мы решаем</span></h2>
            <p style="text-align: center; max-width: 800px; margin: 0 auto 50px; font-size: 1.2rem; color: var(--text-gray);" class="fade-in">
                Пчелы играют ключевую роль в нашей экосистеме, но их популяция стремительно сокращается. Мы создаем технологию, которая поможет изменить эту ситуацию.
            </p>

            <div class="mission-grid">
                <div class="mission-card fade-in">
                    <i class="fas fa-skull-crossbones mission-icon"></i>
                    <h3>Массовая гибель</h3>
                    <p>Ежегодно пчеловоды теряют до 40% своих пчелосемей из-за болезней и паразитов</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-clock mission-icon"></i>
                    <h3>Позднее обнаружение</h3>
                    <p>Болезни часто обнаруживаются слишком поздно, когда спасти пчелосемью уже невозможно</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-dollar-sign mission-icon"></i>
                    <h3>Экономические потери</h3>
                    <p>Каждая потерянная пчелосемья стоит около 5000₽, а также влияет на урожайность культур</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Solution Section -->
    <section class="section" style="background: linear-gradient(135deg, var(--dark-bg) 0%, rgba(45,45,45,0.95) 100%);">
        <div class="container">
            <h2 class="section-title fade-in">Наше <span class="highlight">Решение</span></h2>

            <div class="tech-stack">
                <div class="tech-item fade-in">
                    <i class="fas fa-video tech-icon"></i>
                    <h3>Видеомониторинг</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Камеры наблюдения у летков ульев записывают поведение пчел 24/7</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-brain tech-icon"></i>
                    <h3>ИИ-анализ</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Нейросеть анализирует поведение и выявляет ранние признаки заболеваний</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-bell tech-icon"></i>
                    <h3>Мгновенные уведомления</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Пчеловод получает оповещение на смартфон при обнаружении проблем</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-chart-line tech-icon"></i>
                    <h3>Аналитика</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Подробные отчеты и рекомендации по лечению и профилактике</p>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section class="section">
        <div class="container">
            <h2 class="section-title fade-in">Как это <span class="highlight">работает</span></h2>

            <div class="goals-grid">
                <div class="goal-item fade-in">
                    <div class="goal-number">01</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Установка камер</h3>
                        <p style="color: var(--text-gray);">Компактные камеры устанавливаются у летков ульев для круглосуточного наблюдения</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">02</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Сбор данных</h3>
                        <p style="color: var(--text-gray);">Система собирает видео и данные о поведении пчел, активности улья</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">03</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Анализ ИИ</h3>
                        <p style="color: var(--text-gray);">Нейросеть анализирует данные и выявляет аномалии в поведении пчел</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">04</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Уведомления</h3>
                        <p style="color: var(--text-gray);">Пчеловод получает мгновенное оповещение о проблемах на смартфон</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">05</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Рекомендации</h3>
                        <p style="color: var(--text-gray);">Система предлагает рекомендации по лечению и профилактике</p>
                    </div>
                </div>

                <div class="goal-item fade-in">
                    <div class="goal-number">06</div>
                    <div>
                        <h3 style="color: var(--text-light); margin-bottom: 10px;">Предотвращение</h3>
                        <p style="color: var(--text-gray);">Раннее вмешательство спасает пчелосемью от гибели</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Benefits -->
    <section class="section" style="background: linear-gradient(135deg, rgba(45,45,45,0.95) 0%, var(--dark-bg) 100%);">
        <div class="container">
            <h2 class="section-title fade-in">Преимущества <span class="highlight">BeeProtect</span></h2>

            <div class="mission-grid">
                <div class="mission-card fade-in">
                    <i class="fas fa-chart-line mission-icon"></i>
                    <h3>Экономия средств</h3>
                    <p>Снижение потерь пчелосемей на 40% экономит тысячи рублей ежегодно</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-clock mission-icon"></i>
                    <h3>Экономия времени</h3>
                    <p>Автоматический мониторинг освобождает время пчеловода для других задач</p>
                </div>

                <div class="mission-card fade-in">
                    <i class="fas fa-seedling mission-icon"></i>
                    <h3>Защита экосистемы</h3>
                    <p>Сохранение популяции пчел важно для опыления растений и экологического баланса</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Technology Stack -->
    <section class="section">
        <div class="container">
            <h2 class="section-title fade-in">Технологический <span class="highlight">стек</span></h2>

            <div class="tech-stack">
                <div class="tech-item fade-in">
                    <i class="fab fa-python tech-icon"></i>
                    <h3>Python & TensorFlow</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Разработка нейросетевых моделей для анализа поведения</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-cloud tech-icon"></i>
                    <h3>Облачные вычисления</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Обработка и хранение больших объемов видео-данных</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-mobile-alt tech-icon"></i>
                    <h3>Мобильное приложение</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Удобный интерфейс для пчеловодов на iOS и Android</p>
                </div>

                <div class="tech-item fade-in">
                    <i class="fas fa-server tech-icon"></i>
                    <h3>Edge Computing</h3>
                    <p style="color: var(--text-gray); margin-top: 10px;">Локальная обработка данных для снижения задержек</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="section" style="background: linear-gradient(135deg, var(--dark-bg) 0%, rgba(45,45,45,0.95) 100%);">
        <div class="container">
            <h2 class="section-title fade-in">Интересует <span class="highlight">BeeProtect?</span></h2>
            <p style="text-align: center; max-width: 600px; margin: 0 auto 50px; font-size: 1.2rem; color: var(--text-gray);" class="fade-in">
                Хотите внедрить BeeProtect на своей пасеке? Оставьте email, и мы свяжемся с вами!
            </p>

            <div class="contact-form fade-in" style="max-width: 500px; margin: 0 auto;">
                <input type="email" class="contact-input" placeholder="Ваш email" style="width: 100%; margin-bottom: 20px;">
                <button class="cta-button" style="width: 100%;">
                    <i class="fas fa-paper-plane"></i>
                    Отправить заявку
                </button>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="logo">
                    <i class="fas fa-bee" style="font-size: 2rem; color: var(--primary-yellow);"></i>
                    <h2 style="background: linear-gradient(45deg, var(--primary-yellow), var(--accent-orange)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2rem;">BeeProtect</h2>
                </div>

                <div class="nav-links">
                    <a href="/company" class="nav-link">Наша команда</a>
                    <a href="/project" class="nav-link active">Наш проект</a>
                </div>

                <p style="color: var(--text-gray); max-width: 600px; margin: 0 auto; text-align: center;">
                    Инновационная система мониторинга здоровья пчелосемей с использованием искусственного интеллекта
                </p>

                <div class="social-links">
                    <a href="#" class="social-link">
                        <i class="fab fa-telegram"></i>
                    </a>
                    <a href="#" class="social-link">
                        <i class="fab fa-vk"></i>
                    </a>
                    <a href="https://github.com" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="mailto:amal-makhmutov@mail.ru" class="social-link">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>

                <p class="copyright">© 2024 BeeProtect. Все права защищены.</p>
            </div>
        </div>
    </footer>

    {{ common_script }}
</body>
</html>
'''

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Определяем какую страницу показывать
    if path == '' or path == 'company':
        html = company_html.replace('{{ common_style }}', common_style).replace('{{ common_script }}',
                                                                                common_script)
        return render_template_string(html)
    elif path == 'project':
        html = project_html.replace('{{ common_style }}', common_style).replace('{{ common_script }}',
                                                                                common_script)
        return render_template_string(html)
    else:
        # Для любых других путей - перенаправляем на главную
        html = company_html.replace('{{ common_style }}', common_style).replace('{{ common_script }}',
                                                                                common_script)
        return render_template_string(html)

# ВАЖНО для Vercel: создаем handler
# Vercel будет искать переменную `handler` или функцию `app`
handler = app

# Альтернативно, можно использовать:
# app = handler
