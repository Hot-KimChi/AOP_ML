import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Sidebar({ active }) {
  const router = useRouter();

  const menuItems = [
    { href: '/measset-generation', icon: 'fas fa-cogs', text: 'MeasSet Generation' },
    { href: '/viewer', icon: 'fas fa-eye', text: 'Viewer' },
    { href: '/verification-report', icon: 'fas fa-clipboard-check', text: 'Verification Report' },
    { href: '/machine-learning', icon: 'fas fa-brain', text: 'Machine Learning' },
  ];

  return (
    <nav id="sidebar" className={`col-md-3 col-lg-2 d-md-block bg-light sidebar ${active ? 'active' : ''}`}>
      <div className="position-sticky sidebar-sticky">
        <ul className="nav flex-column">
          {menuItems.map((item, index) => (
            <li className="nav-item" key={index}>
              <Link href={item.href}>
                <a className={`nav-link ${router.pathname === item.href ? 'active' : ''}`}>
                  <i className={item.icon}></i> {item.text}
                </a>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
